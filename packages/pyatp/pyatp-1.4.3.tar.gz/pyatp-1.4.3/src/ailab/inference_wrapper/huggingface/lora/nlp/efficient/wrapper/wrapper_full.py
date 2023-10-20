#!/usr/bin/env python
# coding:utf-8
"""
@license: Apache License2
@file: wrapper.py
@time: 2022-08-19 02:05:07.467170
@project: mnist
@project: ./
"""
import os.path
import threading
from aiges.core.types import *
try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls

from aiges.sdk import WrapperBase, \
    ImageBodyField, \
    StringBodyField, StringParamField
from aiges.utils.log import log, getFileLogger

# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = StringBodyField(key="text", value=b"I have a problem with my iphone that needs to be resolved asap!!")


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key="result")


# 定义服务推理逻辑
class Wrapper(WrapperBase):
    serviceId = "effcient"
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filelogger = None
        self.model = None
        self.tokenizer = None
        self.resid_map = {}
        self.first_load_lora = True
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        #log.info("Initializing ...")
        from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
        base_model_path = os.environ.get("PRETRAINED_MODEL_NAME")
        base_tokenizer_path = os.environ.get("TOKENIZER_PATH")
        full_model_path = os.environ.get("FULL_MDOEL_PATH")
        if not base_model_path or not base_tokenizer_path or not full_model_path:
            log.error("should have environ(PRETRAINED_MODEL_NAME,MODEL_PATH(lora weight dir）,TOKENIZER_PATH)")
            return -1

        def load_model_tokenizer(model_path, tokenizer_path):
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
            model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True)
            return model,tokenizer

        self.base_model, self.base_tokenizer = load_model_tokenizer(base_tokenizer_path,base_model_path)
        self.full_model, self.full_tokenizer = load_model_tokenizer(full_model_path,full_model_path)
        self.filelogger = getFileLogger()
        self.filelogger.info("wrapperInit end")
        return 0

    def _base_model_inference(self, reqData: DataListCls) -> str:
        tokenizer = self.base_tokenizer
        model = self.base_model

        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)
        inputs = tokenizer(input_text, return_tensors='pt')
        gen_kwargs = {
                "max_new_tokens": 512,
                "repetition_penalty": 1.1,
            }
        
        model_name = os.environ.get("PetrainedModel")
        from ailab.atp_finetuner.constant import Model
        input_ids_model = [Model.xverse_13b,Model.falcon_7b,Model.llama2_7b]
        if model_name in input_ids_model:
            inputs = inputs.input_ids
            inputs = inputs.to(model.device)
            output = model.generate(inputs, **gen_kwargs)
        else:
            inputs = inputs.to(model.device)
            output = model.generate(**inputs, **gen_kwargs)
        output = tokenizer.decode(output[0], skip_special_tokens=True)
        return output

    def _full_model_infence(self, reqData: DataListCls) -> str:
        model_name = os.environ.get("PetrainedModel")
        if not model_name:
            log.error("should have environ PetrainedModel")
            return None
        tokenizer = self.full_tokenizer
        model = self.full_model

        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)

        from transformers import TextIteratorStreamer
        from ailab.utils.template import Template
        from ailab.atp_finetuner.constant import Model
        from threading import Thread

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

        prompt_template = Template(template_dict.get(model_name))
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
                print(new_text, end="", flush=True)
                response += new_text
            print()

            return response

        result = predict_and_print(input_text)
        return result

    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag:str="",persId: int = 0) -> Response:
        patch_id = params.get("atp_patch_id", 0)
        self.filelogger.info("got reqdata , %s" % reqData.list)
        self.lock.acquire()
        if patch_id == 0 or patch_id == "0":
            result = self._base_model_inference(reqData)
        else:
            result = self._full_model_infence(reqData)
        self.lock.release()
        if not result:
            self.filelogger.info("#####")
            return -1

        self.filelogger.info("got result , %s" % result)
        # 使用Response封装result
        res = Response()
        resd = ResponseData()
        resd.key = "result"
        resd.setDataType(DataText)
        resd.status = Once
        resd.setData(result.encode("utf-8"))
        print("###")
        self.filelogger.info("###")

        self.filelogger.info(result)
        print(result)
        res.list = [resd]
        return res

    def wrapperFini(cls) -> int:
        return 0

    def wrapperError(cls, ret: int) -> str:
        if ret == 100:
            return "user error defined here"
        return ""

    '''
        此函数保留测试用，不可删除
    '''

    def wrapperTestFunc(cls, data: [], respData: []):
        pass


if __name__ == '__main__':
    m = Wrapper()
    m.run()
