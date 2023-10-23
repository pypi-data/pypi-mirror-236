from aiges.dto import Response, ResponseData, DataListNode, DataListCls

"""personal param"""
model_name = 'chatglm2_6b'
pretrain_model_name = '/home/sdk_models/chatglm2_6b'
token_path = '/home/sdk_models/chatglm2_6b'
full_path = '/opt/ailab_sdk/src/test/ailabmodel/my_chatglm2_model_full'
module_name = 'chatglm'
""""""

import sys
print(sys.path)

import importlib
module_path = f'ailab.inference_wrapper.huggingface.lora.nlp.{module_name}.wrapper.wrapper_full'
wrapper_module = importlib.import_module(module_path)
Wrapper = getattr(wrapper_module, 'Wrapper')
wrapper = Wrapper()

def Init():
    import os
    os.environ['PRETRAINED_MODEL_NAME'] = pretrain_model_name
    os.environ['TOKENIZER_PATH'] = token_path
    os.environ['FULL_MDOEL_PATH'] = full_path
    wrapper.wrapperInit({})

def Once(key, text):
    http_node = DataListNode()
    http_node.key = 'text'
    text_data = text
    text_data = text_data.encode('utf-8')
    http_node.data = text_data 
    http_data = DataListCls()
    http_data.list.append(http_node)

    import os
    os.environ['PetrainedModel'] = model_name
    wrapper.wrapperOnceExec({"atp_patch_id":key}, http_data, key)


if __name__ == '__main__' :
    Init()
    Once(0, '自然语言处理是什么')
    Once(1, '自然语言处理是什么')


