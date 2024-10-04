import pyaudio
import socket

# 音频参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# 网络设置
SERVER_HOST = '192.168.1.8'  # 服务端IP地址
SERVER_PORT = 12345

def audio_stream():
    p = pyaudio.PyAudio()
    
    # 打开音频流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    return p, stream

def main():
    p, stream = audio_stream()
    
    # 创建socket连接
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    print(f"已连接到服务器 {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            data = stream.read(CHUNK)
            client_socket.sendall(data)
    except KeyboardInterrupt:
        print("客户端正在关闭...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()

if __name__ == "__main__":
    main()
