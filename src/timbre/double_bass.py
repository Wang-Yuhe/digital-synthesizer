"""低音提琴音色"""
import numpy as np
from src.timbre.adsr import apply_adsr

def rms_normalize(waveform):
    """使用RMS归一化波形"""
    rms = np.sqrt(np.mean(waveform**2))
    if rms > 0:
        return waveform / rms
    return waveform

def double_bass(freq, duration, sample_rate, volume):
    """低音提琴音色"""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # 调整谐波成分，以接近低音提琴的音色
    harmonics = [1.0, 0.3, 0.1]  # 减少高频成分，强调低频
    waveform = sum(volume * amplitude * np.sin(2 * np.pi * freq * (i + 1) * t)
                        for i, amplitude in enumerate(harmonics))

    # 增加低频噪声以增强低频特性
    noise_amplitude = 0.3  # 增加噪声幅度以增强低频特性
    noise = np.random.normal(0, noise_amplitude, len(t))

    # 低通滤波器：使用简单的移动平均来增强低频噪声
    window_size = 150  # 增加窗口大小以增强低频特性
    low_pass_noise = np.convolve(noise, np.ones(window_size) / window_size, mode='same')

    waveform += low_pass_noise

    # 增加颤音效果以增加不稳定性
    vibrato_depth = 0.03
    vibrato_rate = 8
    vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
    waveform *= vibrato

    # 归一化
    waveform /= np.max(np.abs(waveform))

    # 增加非线性失真以增加粗糙感
    waveform = np.tanh(1.5 * waveform)  # 适度增加失真系数

    # 应用ADSR包络，模仿低音提琴的发音特性
    attack_time = duration * 0.1
    decay_time = duration * 0.2
    sustain_level = 0.5
    release_time = duration * 0.7
    apply_adsr(waveform,sample_rate, attack_time, decay_time, sustain_level, release_time)

    return rms_normalize(waveform)
