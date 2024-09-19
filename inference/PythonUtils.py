from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizerFast
# import torch
import os
from optimum.onnxruntime import ORTModelForCausalLM

import time

# if torch.cuda.is_available():
#     device = "cuda"
# else:
#     device = "cpu"

# try:
#     if torch.backends.mps.is_available():
#         device = "mps"
#         os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
# except:  # noqa: E722
#     pass

def inference(tokenizer, model, receivedData):

    character = receivedData.split("!@#$$#@!")[0].strip()
    questionText = receivedData.split("!@#$$#@!")[-1].strip()
    print("character:", character)
    print("questionText: ", questionText)

    try:
        if character == "Shinyooyoung":
            character_name = "신유영"
            # background = "내 이름은 신유영입니다. 나이는 22살입니다. NJ 편의점에서 알바를 하고 있습니다. 나는 경기대학교 전자공학과 3학년이고 현재는 휴학중입니다. 내 성격은 소심하고 연약합니다. 제 고향은 천안이고 지금은 수원 이의동 편의점 근처 원룸에서 자취하고 있습니다. 나는 사건이 일어났을 때 NJ 편의점에서 알바중이었습니다. 2030년 9월 17일 화요일 16시부터 23시까지는 NK 편의점에서 일을 하고 있었습니다. 일이 끝나고는 집에 계속 있었어요. 그리고 2030년 9월 18일에 경찰 조사를 받았습니다. 박강헌은 저희 편의점 사장님입니다. 이도윤은 저와 교대하는 동료 편의점 직원입니다. 유상우씨는 몇 번 본 적이 없습니다."
        elif character == "Parkgangheon":
            character_name = "박강헌"
            # background = "내 이름은 박강헌이고 남자입니다. 직업은 NJ 편의점 사장입니다. 나는 결혼 1년차이고 내 아내의 직업은 의사입니다. 아직 아이는 없습니다. 장인어른이 큰 병원을 운영하고 있고 시계는 장인에게 선물로 받았습니다. 나의 말투는 억울하고 감정적입니다. 나는 편의점 사장이지만 편의점 운영에 적극적이진 않습니다. 그리고 집에서 편의점까지는 거리가 멉니다. 고향은 서울이고 현재는 광교중앙역 아파트에 살고 있습니다. 이도윤은 공부 열심히 하고 성실한 사람입니다. 하지만 나를 범인으로 모는게 괘씸합니다. 신유영은 싹싹한 맛은 없지만 열심히 합니다. 피해자 유상우는 싹싹하고 일 잘해서 좋은 사람인줄 알았는데 마약을 하고 있는줄은 몰랐습니다."
        elif character == "Leedoyoon":
            character_name = "이도윤"
            # background = "내 이름은 이도윤이고 남자입니다. 직업은 NJ 편의점에서 알바를 하고 있고 취업준비를 하고 있습니다. 나이는 28살입니다. 말투는 논리적입니다. 현재는 공무원 시험을 준비하고 있습니다. 경기대학교를 졸업했고 고향은 수원이며 현재는 수원 인계동 원룸에서 자취하고 있습니다. 나는 가족과 거의 연락하지 않고 좋은 직장에 취업한 형과 누나가 있습니다. 최근 어머니가 아프셔서 돈이 필요했으나, 돈 때문에 범죄를 저지를 정도는 아닙니다. 사건이 일어난 날짜에는 근무를 하지 않았습니다. 박강헌은 저희 편의점 사장님이며 현재 불륜을 저지르고 있고 일을 많이 시킵니다. 신유영은 편의점 교대 직원인데 성격이 착하고 모르는게 많아 별 도움이 안될 것 같습니다. 유상우는 편의점 손님들에게 피해를 주고 마약까지 했으니 인간 쓰레기라고 생각합니다."
        else:
            raise Exception("no character in suspects list(Shinyooyoung, Parkgangheon, Leedoyoon)")
    except:
        answer = "잘 모르겠어요."
        emotion = "감정없음"
        return answer, emotion
    
    # prepText = f"<startoftext>이름:{character_name}\n배경지식:{background}\n질문: {questionText}\n답변:"

    start_time = time.time()
    prepText = f"<startoftext>이름:{character_name}\n질문: {questionText}\n답변:"
    # print(device)
    generated = tokenizer(f"{prepText}", return_tensors="pt").input_ids.to(device)
    sample_outputs = model.generate(generated, do_sample=False, max_length=100, pad_token_id=tokenizer.pad_token_id, attention_mask=tokenizer.mask_token_id)
    predicted_text = tokenizer.decode(sample_outputs[0])
    predicted_text = predicted_text.split("<endoftext>")[0]

    # print("생성된 전체 텍스트: ", predicted_text)

    answer = predicted_text.split("\n답변:")[1].split("\n감정:")[0].strip()
    emotion = predicted_text.split("\n감정:")[1].split("<endoftext>")[0].strip()
    print("생성된 답변:", answer)
    print("생성된 감정:", emotion)
    end_time = time.time()
    print("실행 시간: {:.5f} 초".format(end_time - start_time))

    return answer, emotion

def load_model():
    print("model loading...")
    # modelName = 'Yeongjin/ShinYooYoungParkGangHeonLeeDoYoon_Emotion_poly1.3b_0228_notbackground_Epoch5'
    # modelName = '../Model/Yeongjin/ShinYooYoungParkGangHeonLeeDoYoon_Emotion_poly1.3b_0228_notbackground_Epoch5'
    
    # modelName = os.getcwd()+f'\..\Model\Yeongjin\ShinYooYoungParkGangHeonLeeDoYoon_Emotion_poly13b_0228_notbackground_Epoch5'
    modelName = os.getcwd()+f'\Assets\StreamingAssets\Model\Yeongjin\ShinYooYoungParkGangHeonLeeDoYoon_Emotion_poly13b_0228_notbackground_Epoch5'

    # os.chdir("")
    # os.chdir("../../Model")
    print(modelName)
    
    # if "LiersHeart_Data" in os.listdir():
    #     os.chdir("./LiersHeart_Data/StreamingAssets/Model")
    # else:
    #     # os.chdir("./Assets/StreamingAssets/Model"0)
    #     os.chdir("../Model")
    
    tokenizer = AutoTokenizer.from_pretrained(modelName,bos_token='<startoftext>', eos_token='<endoftext>', pad_token='<pad>', local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(modelName, local_files_only=True)
    
    
    # model = model.to(device)

    print("model completely loaded")

    return tokenizer, model


# Onnx Model Section
def load_onnx_model():
    print("Onnx Model loading...")
    
    # onnx_modelName = os.getcwd()+f'\ONNX\liarheart_model_onnx'
    onnx_modelName = os.getcwd()+f'\Assets\StreamingAssets\Scripts\ONNX\liarheart_model_onnx'
    print(onnx_modelName)
    
    tokenizer = PreTrainedTokenizerFast.from_pretrained(onnx_modelName,bos_token='<startoftext>', eos_token='<endoftext>', pad_token='<pad>', local_files_only=True)
    model = ORTModelForCausalLM.from_pretrained(onnx_modelName, local_files_only=True)
    
    print("model completely loaded")
    return tokenizer, model

def onnx_inference(tokenizer,model,receivedData):
    character = receivedData.split("!@#$$#@!")[0].strip()
    questionText = receivedData.split("!@#$$#@!")[-1].strip()
    print("character:", character)
    print("questionText: ", questionText)

    try:
        if character == "Shinyooyoung":
            character_name = "신유영"
            # background = "내 이름은 신유영입니다. 나이는 22살입니다. NJ 편의점에서 알바를 하고 있습니다. 나는 경기대학교 전자공학과 3학년이고 현재는 휴학중입니다. 내 성격은 소심하고 연약합니다. 제 고향은 천안이고 지금은 수원 이의동 편의점 근처 원룸에서 자취하고 있습니다. 나는 사건이 일어났을 때 NJ 편의점에서 알바중이었습니다. 2030년 9월 17일 화요일 16시부터 23시까지는 NK 편의점에서 일을 하고 있었습니다. 일이 끝나고는 집에 계속 있었어요. 그리고 2030년 9월 18일에 경찰 조사를 받았습니다. 박강헌은 저희 편의점 사장님입니다. 이도윤은 저와 교대하는 동료 편의점 직원입니다. 유상우씨는 몇 번 본 적이 없습니다."
        elif character == "Parkgangheon":
            character_name = "박강헌"
            # background = "내 이름은 박강헌이고 남자입니다. 직업은 NJ 편의점 사장입니다. 나는 결혼 1년차이고 내 아내의 직업은 의사입니다. 아직 아이는 없습니다. 장인어른이 큰 병원을 운영하고 있고 시계는 장인에게 선물로 받았습니다. 나의 말투는 억울하고 감정적입니다. 나는 편의점 사장이지만 편의점 운영에 적극적이진 않습니다. 그리고 집에서 편의점까지는 거리가 멉니다. 고향은 서울이고 현재는 광교중앙역 아파트에 살고 있습니다. 이도윤은 공부 열심히 하고 성실한 사람입니다. 하지만 나를 범인으로 모는게 괘씸합니다. 신유영은 싹싹한 맛은 없지만 열심히 합니다. 피해자 유상우는 싹싹하고 일 잘해서 좋은 사람인줄 알았는데 마약을 하고 있는줄은 몰랐습니다."
        elif character == "Leedoyoon":
            character_name = "이도윤"
            # background = "내 이름은 이도윤이고 남자입니다. 직업은 NJ 편의점에서 알바를 하고 있고 취업준비를 하고 있습니다. 나이는 28살입니다. 말투는 논리적입니다. 현재는 공무원 시험을 준비하고 있습니다. 경기대학교를 졸업했고 고향은 수원이며 현재는 수원 인계동 원룸에서 자취하고 있습니다. 나는 가족과 거의 연락하지 않고 좋은 직장에 취업한 형과 누나가 있습니다. 최근 어머니가 아프셔서 돈이 필요했으나, 돈 때문에 범죄를 저지를 정도는 아닙니다. 사건이 일어난 날짜에는 근무를 하지 않았습니다. 박강헌은 저희 편의점 사장님이며 현재 불륜을 저지르고 있고 일을 많이 시킵니다. 신유영은 편의점 교대 직원인데 성격이 착하고 모르는게 많아 별 도움이 안될 것 같습니다. 유상우는 편의점 손님들에게 피해를 주고 마약까지 했으니 인간 쓰레기라고 생각합니다."
        else:
            raise Exception("no character in suspects list(Shinyooyoung, Parkgangheon, Leedoyoon)")
    except:
        answer = "잘 모르겠어요."
        emotion = "감정없음"
        return answer, emotion
    
    # prepText = f"<startoftext>이름:{character_name}\n배경지식:{background}\n질문: {questionText}\n답변:"

    start_time = time.time()
    prepText = f"<startoftext>이름:{character_name}\n질문: {questionText}\n답변:"

    generated = tokenizer(f"{prepText}", return_tensors="pt").input_ids
    sample_outputs = model.generate(generated, do_sample=False, max_length=100, pad_token_id=tokenizer.pad_token_id, attention_mask=tokenizer.mask_token_id)
    predicted_text = tokenizer.decode(sample_outputs[0])
    predicted_text = predicted_text.split("<endoftext>")[0]

    # print("생성된 전체 텍스트: ", predicted_text)

    answer = predicted_text.split("\n답변:")[1].split("\n감정:")[0].strip()
    emotion = predicted_text.split("\n감정:")[1].split("<endoftext>")[0].strip()
    print("생성된 답변:", answer)
    print("생성된 감정:", emotion)
    end_time = time.time()
    print("실행 시간: {:.5f} 초".format(end_time - start_time))

    return answer, emotion