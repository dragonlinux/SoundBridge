import pyaudio
import socket
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
            return config['SERVER_HOST'], config['SERVER_PORT']
    except FileNotFoundError:
        print("配置文件 'configure.json' 未找到。使用默认设置。")
        return '127.0.0.1', 12345
    except json.JSONDecodeError:
        print("配置文件格式错误。使用默认设置。")
        return '127.0.0.1', 12345
    except KeyError:
        print("配置文件缺少必要的键。使用默认设置。")
        return '127.0.0.1', 12345

SERVER_HOST, SERVER_PORT = load_config()

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
