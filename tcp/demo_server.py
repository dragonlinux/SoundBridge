import pyaudio
import socket
import threading
import json

# 音频参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# 从配置文件读取网络设置
def load_config():
    try:
        with open('configure.json', 'r') as config_file:
            config = json.load(config_file)
            return config['HOST'], config['PORT']
    except FileNotFoundError:
        print("配置文件 'configure.json' 未找到。使用默认设置。")
        return '127.0.0.1', 12345
    except json.JSONDecodeError:
        print("配置文件格式错误。使用默认设置。")
        return '127.0.0.1', 12345
    except KeyError:
        print("配置文件缺少必要的键。使用默认设置。")
        return '127.0.0.1', 12345

HOST, PORT = load_config()

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
