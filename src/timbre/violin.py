"""小提琴音色"""
import numpy as np
from src.timbre.adsr import apply_adsr

def rms_normalize(waveform):
    """使用RMS归一化波形"""
    rms = np.sqrt(np.mean(waveform**2))
    if rms > 0:
        return waveform / rms
    return waveform

def violin(freq, duration, sample_rate, volume):
    """小提琴音色"""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # 小提琴的谐波成分更丰富，高频部分衰减较慢
    harmonics = [0.5, 0.8, 0.3, 0.15, 0.1, 0.08, 0.05, 0.03, 0.02, 0.01]  # 基频相对较弱，谐波更丰富
    waveform = sum(volume * amplitude * np.sin(2 * np.pi * freq * (i + 1) * t)
                        for i, amplitude in enumerate(harmonics))
    vibrato_depth = 0.02  # 颤音深度
    vibrato_rate = 6  # 颤音频率(Hz)
    vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
    waveform *= vibrato
    waveform /= np.max(np.abs(waveform))

    # 小提琴的ADSR包络 - 更慢的起音和释音
    attack_time = duration * 0.1  # 更长的起音时间
    decay_time = duration * 0.2  # 更长的衰减时间
    sustain_level = 0.7  # 较高的持续电平
    release_time = duration * 0.3  # 更长的释音时间

    apply_adsr(waveform,sample_rate,attack_time, decay_time, sustain_level, release_time)
    return rms_normalize(waveform)
