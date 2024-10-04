import pyaudio
import socket
import numpy as np
from scipy import signal
import webrtcvad

# 音频参数
CHUNK = 960  # 60ms at 16kHz, 增加以适应可能的较大数据包
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# 网络设置
HOST = '192.168.1.8'  # 服务端IP地址
PORT = 12345

vad = webrtcvad.Vad(3)  # 设置 VAD 的攻击性 (0-3)

def audio_stream():
    p = pyaudio.PyAudio()
    
    # 打开音频流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    return p, stream

def high_pass_filter(data, cutoff=100, fs=RATE):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(5, normal_cutoff, btype='high', analog=False)
    data = np.frombuffer(data, dtype=np.int16)
    filtered = signal.filtfilt(b, a, data)
    return filtered.astype(np.int16)

def process_audio(audio):
    # 高通滤波
    audio = high_pass_filter(audio)
    
    # 降低音量
    audio = (audio * 0.5).astype(np.int16)
    
    # VAD 处理
    is_speech = vad.is_speech(audio[:480].tobytes(), RATE)  # 只处理前30ms
    
    if is_speech:
        return audio.tobytes()
    else:
        return np.zeros(len(audio), dtype=np.int16).tobytes()

def main():
    p, stream = audio_stream()
    
    # 创建UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    
    # 增加接收缓冲区大小
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
    
    print(f"服务器正在监听 {HOST}:{PORT}")

    try:
        while True:
            data, addr = server_socket.recvfrom(CHUNK * 2)  # *2 因为每个样本是2字节
            processed_data = process_audio(data)
            stream.write(processed_data)
    except KeyboardInterrupt:
        print("服务器正在关闭...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        server_socket.close()

if __name__ == "__main__":
    main()
