import argparse, subprocess, torch, os
from ailab.log import logger
from ailab.atp_finetuner.constant import Model

try:
    import jsonlines
except ImportError:
    print("jsonlines not install.please use 'pip install jsonlines'")

def read_input_file(input_file_path:str):
    lines = []
    try:
        with open(input_file_path, "r", encoding="utf-8") as file:
            for line in file:
                # 去除行尾的换行符并添加到数组中
                lines.append(line.strip())
    except FileNotFoundError:
        logger.error(f"file '{input_file_path}' not found.")
    return lines

def write_output_file(output_file_path:str, querys:[], answers:[]):
    with jsonlines.open(output_file_path, 'w') as jsonl_file:
        for query, answer in zip(querys, answers):
            json_object = {"input": query, "output": answer}
            jsonl_file.write(json_object)

def common_base_model_pipeline(model, tokenizer, args):
    output_file_path = args.base_result_path
    input_file_path = args.test_dataset_path

    querys = read_input_file(input_file_path)
    answers = []
    for input_text in querys:
        inputs = tokenizer(input_text, return_tensors='pt')
        gen_kwargs = {
                "max_new_tokens": 512,
                "repetition_penalty": 1.1,
            }
        
        input_ids_model = [Model.xverse_13b,Model.falcon_7b,Model.llama2_7b]
        if args.pretrained_model_name in input_ids_model:
            inputs = inputs.input_ids
            inputs = inputs.to(model.device)
            output = model.generate(inputs, **gen_kwargs)
        else:
            inputs = inputs.to(model.device)
            output = model.generate(**inputs, **gen_kwargs)
        output = tokenizer.decode(output[0], skip_special_tokens=True)
        answers.append(output)
    write_output_file(output_file_path, querys, answers)

def chatglm_base_model_pipeline(model, tokenizer, args):
    output_file_path = args.base_result_path
    input_file_path = args.test_dataset_path
    querys = read_input_file(input_file_path)
    answers = []

    for input_text in querys:
        response, history = model.chat(tokenizer, input_text, history=[])
        answers.append(response)
    write_output_file(output_file_path, querys, answers)


def load_chatglm_model_tokenizer(model_path,tokenizer_path):
    from transformers import AutoTokenizer,AutoConfig,AutoModel
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_path,
        use_fast=False,
        padding_side="left",
        trust_remote_code=True
    )

    config = AutoConfig.from_pretrained(model_path,trust_remote_code=True)
    model = AutoModel.from_pretrained(model_path, config=config, 
                                      trust_remote_code=True, device_map="auto")
    assert tokenizer.eos_token_id is not None, "Please update the *.json and *.py files of ChatGLM-6B from HuggingFace."
    model.requires_grad_(False) # fix all model params
    model = model.half() # cast all params to float16 for inference
    model = model.cuda()
    model.eval()
    return model,tokenizer

#chatglm1 and chatglm2
def chatglm_pipeline(args):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    base_model,base_tokenizer = load_chatglm_model_tokenizer(args.pretrained_model_path, args.tokenizer_path)
    chatglm_base_model_pipeline(base_model,base_tokenizer,args)

    if args.finetune_type == 'full':
        model,tokenizer = load_chatglm_model_tokenizer(args.fintuned_weights,args.fintuned_weights)

    if args.finetune_type == 'lora':
        from peft import PeftModel
        tokenizer = base_tokenizer
        model = PeftModel.from_pretrained(base_model, args.fintuned_weights)

    history = []

    generating_args = {
        "do_sample":True,
        "temperature":0.95,
        "top_p":0.9,
        "top_k":60,
        "num_beams":1,
        "max_length":2048,
        "max_new_tokens":None,
        "repetition_penalty":1.1,
    }

    querys = read_input_file(args.test_dataset_path)
    answers = []

    def evalute(query):
        from typing import Optional,List,Tuple
        def get_prompt(query: str, history: Optional[List[Tuple[str, str]]] = None, prefix: Optional[str] = None) -> str:
            prefix = prefix + "\n" if prefix else "" # add separator for non-empty prefix
            history = history or []
            prompt = ""
            for i, (old_query, response) in enumerate(history):
                prompt += "[Round {}]\n\n问：{}\n\n答：{}\n\n".format(i+1, old_query, response)
            prompt += "[Round {}]\n\n问：{}\n\n答：".format(len(history)+1, query)
            prompt = prefix + prompt
            return prompt
        
        prefix = ""
        inputs = tokenizer([get_prompt(query, history, prefix)], return_tensors="pt")
        inputs = inputs.to(model.device)
        input_ids = inputs["input_ids"]

        from transformers import TextIteratorStreamer
        from threading import Thread
        streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
        generating_args.update(dict(input_ids=input_ids,streamer=streamer))
        thread = Thread(target=model.generate, kwargs=generating_args)
        thread.start()

        response = ""
        for new_text in streamer:
            response += new_text

        return response

    for instruction in querys:
        response = evalute(instruction)
        logger.info(f'instruction {instruction}')
        logger.info(f'response {response}')
        answers.append(response)
    write_output_file(args.finetuned_result_path, querys, answers)

def chinese_alpaca_inference(model, tokenizer, lora_weight, args):
    from peft import PeftModel
    if lora_weight is None:
        output_file_path = args.base_result_path
    else:
        model = PeftModel.from_pretrained(model, 
                                    lora_weight,
                                    torch_dtype=torch.float16,
                                    device_map='auto',)
        output_file_path = args.finetuned_result_path

    model.eval()

    device = torch.device(0)
    def evaluate(instruction: str) -> str:
        generation_config = dict(
            temperature=0.2,
            top_k=40,
            top_p=0.9,
            do_sample=True,
            num_beams=1,
            repetition_penalty=1.1,
            max_new_tokens=512,
            )

        # The prompt template below is taken from llama.cpp
        # and is slightly different from the one used in training.
        # But we find it gives better results
        if (len(tokenizer)) == 49954:
            prompt_input = (
                "Below is an instruction that describes a task. "
                "Write a response that appropriately completes the request.\n\n"
                "### Instruction:\n\n{instruction}\n\n### Response:\n\n"
            )
            def generate_prompt(instruction, input=None):
                if input:
                    instruction = instruction + '\n' + input
                return prompt_input.format_map({'instruction': instruction})
        elif (len(tokenizer)) == 55296:
            prompt_input = (
                "[INST] <<SYS>>\n"
                "{system_prompt}\n"
                "<</SYS>>\n\n"
                "{instruction} [/INST]"
            )
            DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant. 你是一个乐于助人的助手。"""
            def generate_prompt(instruction, system_prompt=DEFAULT_SYSTEM_PROMPT):
                return prompt_input.format_map({'instruction': instruction,'system_prompt': system_prompt})


        with torch.no_grad():
            input_text = generate_prompt(instruction=instruction)
            inputs = tokenizer(input_text,return_tensors="pt")  #add_special_tokens=False ?
            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs['attention_mask'].to(device)
            generation_output = model.generate(
                input_ids = input_ids, 
                attention_mask = attention_mask,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id,
                **generation_config
            )
        s = generation_output[0]
        output = tokenizer.decode(s,skip_special_tokens=True)
        if (len(tokenizer)) == 49954:
            response = output.split("### Response:")[1].strip()
        else:
            response = output.split("[/INST]")[-1].strip()
        return response

    querys = read_input_file(args.test_dataset_path)
    answers = []
    
    for instruction in querys:
        logger.info("Instruction:", instruction)
        response = evaluate(instruction)
        logger.info("Response:", response)
        answers.append(response)
    write_output_file(output_file_path, querys, answers)

def chinese_llama_alpaca_pipeline(args):
    if args.finetune_type == 'full':
        raise SystemExit(f'chinese_llama_alpaca not support full yeat')
    
    tokenizer_path = args.tokenizer_path
    base_model = args.pretrained_model_path

    from transformers import LlamaForCausalLM,LlamaTokenizer

    tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path) #, legacy=False
    if (len(tokenizer)) == 55296: #v2 49954:v1
        from ailab.utils.attn_and_long_ctx_patches import apply_attention_patch, apply_ntk_scaling_patch
        apply_attention_patch(use_memory_efficient_attention=True)
        apply_ntk_scaling_patch("1.0")


    model = LlamaForCausalLM.from_pretrained(
        base_model, 
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
        device_map='auto',
        )
    
    # unify tokenizer and embedding size
    model_vocab_size = model.get_input_embeddings().weight.size(0)
    tokenzier_vocab_size = len(tokenizer)
    logger.info(f"Vocab of the base model: {model_vocab_size}")
    logger.info(f"Vocab of the tokenizer: {tokenzier_vocab_size}")
    if model_vocab_size!=tokenzier_vocab_size:
        assert tokenzier_vocab_size > model_vocab_size
        logger.info("Resize model embeddings to fit tokenizer")
        model.resize_token_embeddings(tokenzier_vocab_size)

    chinese_alpaca_inference(model, tokenizer, None, args)
    chinese_alpaca_inference(model, tokenizer, args.fintuned_weights, args)

def load_efficient_model_tokenizer(model_path, tokenizer_path):
    from transformers import AutoTokenizer,AutoModelForCausalLM
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True)
    return model, tokenizer

def LLaMA_Efficient_Tuning_pipeline(args):
    from transformers import TextIteratorStreamer
    from threading import Thread

    base_model,tokenizer = load_efficient_model_tokenizer(args.pretrained_model_path,args.tokenizer_path)
    common_base_model_pipeline(base_model,tokenizer,args)

    if args.finetune_type == 'full':
        model,tokenizer = load_efficient_model_tokenizer(args.fintuned_weights,args.fintuned_weights)

    if args.finetune_type == 'lora':
        from peft import PeftModel
        model = PeftModel.from_pretrained(base_model, args.fintuned_weights)

    from ailab.utils.template import Template
    template_dict = {
        Model.baichuan_7b : "default",
        Model.baichuan_13b : "default",
        Model.bloomz_7b1_mt : "default",
        Model.falcon_7b : "default",
        Model.moss_moon_003_base : "moss",
        Model.llama2_7b : "llama2",
        Model.internlm_7b : "default",
        Model.belle_7b_2m : "belle",
        Model.xverse_13b : "vanilla",
        Model.lawgpt_llama : "alpaca",
    }
    prompt_template = Template(template_dict.get(args.pretrained_model_name))
    source_prefix = ""

    def predict_and_print(query) -> list:
        history = []
        input_ids = tokenizer([prompt_template.get_prompt(query, history, source_prefix)], return_tensors="pt")["input_ids"]
        input_ids = input_ids.to(model.device)

        streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
        gen_kwargs = {
            "input_ids": input_ids,
            "streamer": streamer,
            "do_sample": True,
            "temperature": 0.95,
            "top_p": 0.7,
            "top_k": 50,
            "num_beams": 1,
            "max_new_tokens": 512,
            "repetition_penalty": 1.0,
            "length_penalty": 1.0,
        }

        thread = Thread(target=model.generate, kwargs=gen_kwargs)
        thread.start()

        response = ""
        for new_text in streamer:
            response += new_text

        return response
    
    querys = read_input_file(args.test_dataset_path)
    answers = []
    for instruction in querys:
        logger.info("Instruction:", instruction)
        response = predict_and_print(instruction)
        logger.info("Response:", response)
        answers.append(response)
    write_output_file(args.finetuned_result_path, querys, answers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An example script with command-line arguments.")
    parser.add_argument("--finetune_type", type=str, default=None, choices=['lora', 'full'])
    parser.add_argument("--pretrained_model_name", type=str, default=None)
    parser.add_argument("--pretrained_model_path", type=str, default=None)
    parser.add_argument("--tokenizer_path", type=str, default=None)
    parser.add_argument("--fintuned_weights", type=str, default=None)
    parser.add_argument("--test_dataset_path", type=str, default=None)
    parser.add_argument("--base_result_path", type=str, default=None)
    parser.add_argument("--finetuned_result_path", type=str, default=None)
    args = parser.parse_args()

    logger.info(args)

    args_dict = vars(args)  # 将 argparse 命名空间转换为字典
    for arg_name, arg_value in args_dict.items():
        if arg_value is None:
            raise SystemExit(f'{arg_name} is None')
        
    if not os.path.exists(args.pretrained_model_path) :
        raise SystemExit(f'args.pretrained_model_path {args.pretrained_model_path} not exist')
    elif not os.path.exists(args.tokenizer_path):
        raise SystemExit(f'args.tokenizer_path {args.tokenizer_path} not exist')
    elif not os.path.exists(args.test_dataset_path):
        raise SystemExit(f'args.test_dataset_path {args.test_dataset_path} not exist')
    elif args.fintuned_weights is not None and not os.path.exists(args.fintuned_weights):
        raise SystemExit(f'args.fintuned_weights {args.fintuned_weights} not exist')
    
    if not args.base_result_path.endswith('jsonl') or not args.finetuned_result_path.endswith('jsonl'):
        raise SystemExit('output file should be jsonl')

    efficent_model = [Model.baichuan_7b,Model.baichuan_13b,Model.bloomz_7b1_mt,Model.falcon_7b,
                      Model.moss_moon_003_base,Model.llama2_7b,Model.internlm_7b,Model.belle_7b_2m,
                      Model.xverse_13b,Model.lawgpt_llama]
    glm_model = [Model.chatglm_6b,Model.chatglm2_6b,Model.code_geex_2]
    chinese_alpaca_model = [Model.chinese_alpaca,Model.chinese_alpaca_2]
    alpaca_model = [Model.alpaca,Model.bencao_llama]

    if args.pretrained_model_name in efficent_model:
        LLaMA_Efficient_Tuning_pipeline(args)
    elif args.pretrained_model_name in glm_model:
        chatglm_pipeline(args)
    elif args.pretrained_model_name in chinese_alpaca_model:
        chinese_llama_alpaca_pipeline(args)
    else:
        raise SystemExit(f'model_name {args.pretrained_model_name} not support yeat')

    exit(0)
    