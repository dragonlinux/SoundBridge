import pyaudio
import socket

# 音频参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# 网络设置
HOST = '192.168.1.8'  # 服务端IP地址
PORT = 12345

def audio_stream():
    p = pyaudio.PyAudio()
    
    # 打开音频流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    return p, stream

def main():
    p, stream = audio_stream()
    
    # 创建UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    
    print(f"服务器正在监听 {HOST}:{PORT}")

    try:
        while True:
            data, addr = server_socket.recvfrom(CHUNK * 4)  # 增大缓冲区以适应可能的较大数据包
            stream.write(data)
    except KeyboardInterrupt:
        print("服务器正在关闭...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        server_socket.close()

if __name__ == "__main__":
    main()
