import socket
import time, sys
from PythonUtils import *
import timeit

def llm_server():    
    global shutdown_flag

    start_time = time.time()
    # tokenizer, model = load_model()
    tokenizer, model = load_onnx_model()
    
    end_time = time.time()
    print("실행 시간: {:.5f} 초".format(end_time - start_time))

    server_ip = '127.0.0.1'
    server_port = 25001

    server_socket = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
    server_socket.bind((server_ip, server_port))

    server_socket.listen(1)
    print('클라이언트와 연결을 대기합니다...')

    client_socket, client_address = server_socket.accept()
    print(f'클라이언트가 연결되었습니다. 주소: {client_address}')

    # tokenizer, model = modelInit()
    # python 신호를 제대로 받고 있는지 테스트 (로딩씬에서 쓰려고 만듬)
    # 유니티 connectedTest 함수와 이어짐 
    
    success_connect = "success"
    success_connect = success_connect.encode("UTF-8")
    client_socket.send(success_connect)
    print(client_socket)

    while True:                              
        receivedData = client_socket.recv(1024).decode("UTF-8")
        if receivedData == "":
            continue
        elif receivedData == "@!SHUTDOWN":
            break
        
        print("받은 답변: ",receivedData)
        print("답변 생성중")
        # generatedAnswer, generatedEmotion = inference(tokenizer, model, receivedData)
        generatedAnswer, generatedEmotion = onnx_inference(tokenizer, model, receivedData)
        
        sendData = generatedAnswer + "!@#$$#@!" + generatedEmotion
        sendData = sendData.encode('UTF-8')
        client_socket.send(sendData)

        # time.sleep(1)

    quit()

if __name__ == '__main__':

    try:
        llm_server()
    except KeyboardInterrupt:
        print("Server interrupted.")
    finally:
        print("Server shutting down.")
        
    # start_time = time.time()
    # test_model()
    # end_time = time.time()
    # print("실행 시간: {:.5f} 초".format(end_time - start_time))
        