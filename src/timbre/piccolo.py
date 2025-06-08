"""短笛音色"""
import numpy as np
from src.timbre.adsr import apply_adsr

def piccolo(freq, duration, sample_rate, volume):
    """短笛音色"""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Vibrato 参数
    vibrato_rate = 6  # 颤音速率（Hz）
    vibrato_depth = 0.0005  # 颤音深度（相对主频的百分比）

    # 添加 vibrato 到频率上（调频）
    vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)

    # 谐波系数（高频强调）
    harmonics = [1.0, 0.7, 0.5, 0.35, 0.25, 0.15, 0.08, 0.04, 0.02]

    # 合成波形
    waveform = np.zeros_like(t)
    for n, amp in enumerate(harmonics):
        # 调制每个谐波的频率
        modulated_freq = freq * (n + 1) * vibrato
        waveform += amp * np.sin(2 * np.pi * modulated_freq * t)
    waveform *= volume

    # ADSR 包络
    attack_time = 0.05
    decay_time = 0.1
    sustain_level = 0.6
    release_time = 0.2
    waveform = apply_adsr(waveform, sample_rate, attack_time, decay_time, sustain_level, release_time)

    waveform /= np.max(np.abs(waveform)+1e-12)
    waveform *= volume

    return waveform
