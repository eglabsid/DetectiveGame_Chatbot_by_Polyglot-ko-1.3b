import os
import torch
from transformers import AutoTokenizer,PreTrainedTokenizerFast
from optimum.onnxruntime import ORTModelForCausalLM

import time

character_name = "신유영"
questionText = "요즘 치킨 값이 얼마나하지?"
input_text = f"<startoftext>이름:{character_name}\n질문: {questionText}\n답변:"

onnx_file_path = os.getcwd()+"/../Scripts/ONNX/liarheart_model_onnx"

start_time = time.time()

tokenizer = PreTrainedTokenizerFast.from_pretrained(onnx_file_path,bos_token='<startoftext>', eos_token='<endoftext>', pad_token='<pad>', local_files_only=True)
model = ORTModelForCausalLM.from_pretrained(onnx_file_path)

inputs = tokenizer(f"{input_text}", return_tensors="pt").input_ids
outputs = model.generate(inputs, do_sample=False, max_length=100, pad_token_id=tokenizer.pad_token_id, attention_mask=tokenizer.mask_token_id)

predicted_text = tokenizer.decode(outputs[0])
predicted_text = predicted_text.split("<endoftext>")[0]

print("생성된 전체 텍스트: ", predicted_text)

answer = predicted_text.split("\n답변:")[1].split("\n감정:")[0].strip()
emotion = predicted_text.split("\n감정:")[1].split("<endoftext>")[0].strip()
print("생성된 답변:", answer)
print("생성된 감정:", emotion)

end_time = time.time()
print("실행 시간: {:.5f} 초".format(end_time - start_time))
