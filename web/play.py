import pygame
import numpy as np
from scipy.io.wavfile import write
import tempfile
import os

# 初始化只需一次
pygame.mixer.init()

# 全局播放对象
sound = None
channel = None
tmp_wav_path = None

def play_numpy_waveform(waveform, sample_rate=44100):
    global tmp_wav_path, sound, channel

    # 👉 如果正在播放，则先停止并清理前一次播放
    if channel and channel.get_busy():
        channel.stop()
    if tmp_wav_path and os.path.exists(tmp_wav_path):
        os.remove(tmp_wav_path)
        tmp_wav_path = None

    # 转换为 16-bit PCM
    waveform_int16 = np.int16(waveform / np.max(np.abs(waveform)) * 32767)

    # 创建临时文件（不要自动删除）
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp_wav_path = tmp_file.name
    tmp_file.close()  # 必须关闭才能被别的库访问

    # 写入 WAV 数据
    write(tmp_wav_path, sample_rate, waveform_int16)

    # 加载并播放
    sound = pygame.mixer.Sound(tmp_wav_path)
    channel = sound.play()

def stop_waveform_playback():
    global tmp_wav_path
    if channel:
        channel.stop()
    if tmp_wav_path and os.path.exists(tmp_wav_path):
        os.remove(tmp_wav_path)
        tmp_wav_path = None

"""
def pause_playback():
    if channel and channel.get_busy():
        channel.pause()

def unpause_playback():
    if channel:
        channel.unpause()
"""