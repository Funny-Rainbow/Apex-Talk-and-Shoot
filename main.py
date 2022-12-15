import pyaudio
import wave
import numpy as np
import pyautogui as mouse
from time import sleep

import random
def Monitor():
    CHUNK = 128
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("开始缓存录音")
    print('begin ')
    frames = []
    while (True):
        stream.start_stream()
        #for i in range(0, 100):
        data = stream.read(CHUNK)
        frames.append(data)
        audio_data = np.fromstring(data, dtype=np.short)
        large_sample_count = np.sum( audio_data > 800 )
        temp = np.max(audio_data)
        print(temp)
        if temp > 1000: # | temp <2000
            stream.stop_stream()
            print("检测到信号")
            print('当前阈值：',temp)
            mouse.click(clicks=20, interval=random.uniform(0.01,0.05),button='left')
    stream.stop_stream()
    input("Press Enter key to exit.")
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == '__main__':
    Monitor()