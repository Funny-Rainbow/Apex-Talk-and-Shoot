import pyaudio# 调用麦克风
import wave# 音频格式
import numpy as np# 音频处理
import pyautogui as mouse# 鼠标控制
import win32api# 检测大写锁
import win32con# 检测大写锁
import random# 随机，防止脚本检测
import threading# 线程
from time import sleep


# 0为大写关闭，连点；1为大写开启，按住鼠标左键
Tab = [0]
# 1开火
shoot = [0]

# 获取麦克风音量 函数
def monitor():
    # 设置录音片段的大小格式等
    CHUNK = 512
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
    # 进入音量识别循环
    stream.start_stream()
    while True:
        global temp
        # for i in range(0, 100):
        data = stream.read(CHUNK)
        frames.append(data)
        audio_data = np.fromstring(data, dtype=np.short)
        large_sample_count = np.sum(audio_data > 800)
        temp = np.max(audio_data)
        # print(temp)
        # 如果最近声音大于设定值，这里默认为1000，点击鼠标
        if temp < 2000:
            shoot[0] = 0
        else:
            # 设置鼠标点击次数和时间，为防止识别为脚本，每次点击间隔使用0.01-0.05的随机数
            Tab[0]=win32api.GetKeyState(win32con.VK_CAPITAL)
            shoot[0] = 1
        sleep(0.01)
    # 以下代码非必要无需修改
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# 点击鼠标 函数
def mouseLeftClick(Tab, shoot):
    Tab_temp = Tab[0]
    shoot_temp = shoot[0]
    while True:
        if shoot_temp == 1:
            print('shooting!')
            if Tab_temp == 1:
                mouse.mouseDown(button='left')
                sleep(0.5)
                mouse.mouseUp(button='left')
            elif Tab_temp == 0:
                mouse.click(clicks=50, interval=random.uniform(0.01, 0.02), button='left')
                sleep(0.05)
            else:
                print('error occurs:Tab status wrong')
        print('stop')
        # 只有在状态改变时才赋值
        if Tab_temp != Tab[0] or shoot_temp != shoot[0]:
            Tab_temp = Tab[0]
            shoot_temp = shoot[0]



if __name__ == '__main__':
    # 双线程
    t1 = threading.Thread(target=mouseLeftClick, args=(Tab,shoot,))
    t2 = threading.Thread(target=monitor)
    # 录音加上线程守护
    t2.daemon=True
    t1.start()
    t2.start()


