import pyaudio
import socket
import json

# 音频参数
CHUNK = 960  # 60ms at 16kHz, 与服务器端匹配
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

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
