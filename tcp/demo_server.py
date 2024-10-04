import pyaudio
import socket
import threading

# 音频参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# 网络设置
HOST = '192.168.1.12'  # 服务端IP地址
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

def handle_client(conn, stream):
    while True:
        try:
            data = conn.recv(CHUNK)
            if not data:
                break
            stream.write(data)
        except:
            break
    conn.close()

def main():
    p, stream = audio_stream()
    
    # 创建socket服务器
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    print(f"服务器正在监听 {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"连接来自: {addr}")
            client_thread = threading.Thread(target=handle_client, args=(conn, stream))
            client_thread.start()
    except KeyboardInterrupt:
        print("服务器正在关闭...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        server_socket.close()

if __name__ == "__main__":
    main()
