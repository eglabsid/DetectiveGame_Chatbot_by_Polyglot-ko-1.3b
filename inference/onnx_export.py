import torch
import os
from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForCausalLM

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

# device = "cuda"
# print(device)
# LLM 모델과 토크나이저 로드
# 모델 이름 (필요에 따라 변경)
model_name = '../Model/Yeongjin/ShinYooYoungParkGangHeonLeeDoYoon_Emotion_poly13b_0228_notbackground_Epoch5'
if "LiersHeart_Data" in os.listdir():
    os.chdir("./LiersHeart_Data/StreamingAssets/Model")
else:
    # os.chdir("./Assets/StreamingAssets/Model")
    os.chdir("../Model")

# ONNX 파일로 export

# Load a model from transformers and export it to ONNX
ort_model = ORTModelForCausalLM.from_pretrained(model_name, export=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)

save_directory = os.getcwd()+"/../Scripts/ONNX/liarheart_model_onnx"
print(save_directory)
# Save the onnx model and tokenizer
ort_model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)

print(f"모델이 {save_directory}로 export되었습니다.")