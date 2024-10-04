import pyaudio
import socket

# 音频参数
CHUNK = 960  # 60ms at 16kHz, 与服务器端匹配
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

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
    
    # 创建UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(f"准备发送音频到服务器 {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            data = stream.read(CHUNK)
            client_socket.sendto(data, (SERVER_HOST, SERVER_PORT))
    except KeyboardInterrupt:
        print("客户端正在关闭...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()

if __name__ == "__main__":
    main()
