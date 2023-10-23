#!/bin/bash

python -m ailab.inference \
    --finetune_type lora \
    --pretrained_model_name chinese_llama_alpaca_2_13b \
    --pretrained_model_path /home/sdk_models/chinese-alpaca-2-13b/ \
    --tokenizer_path /home/sdk_models/chinese-alpaca-2-13b/ \
    --fintuned_weights /opt/ailab_sdk/src/test/ailabmodel/my_chinese_alpaca2_13b_model \
    --test_dataset_path /opt/ailab_sdk/src/ailab/inference/test/val.txt \
    --base_result_path /opt/ailab_sdk/src/ailab/inference/base.jsonl \
    --finetuned_result_path /opt/ailab_sdk/src/ailab/inference/finetune.jsonl 