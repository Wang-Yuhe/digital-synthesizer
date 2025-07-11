"""长笛音色"""
import numpy as np
from src.timbre.adsr import apply_adsr

def flute(freq, duration, sample_rate, volume):
    """
    长笛音色

    Args:
        freq (float): 频率
        duration (float): 时值，表示单音的持续时间
        sample_rate (float): 采样率
        volume (float): 音量大小，0~1的范围
    
    Returns:
        waveform (np.ndarray): 合成长笛音色后的波形
    """
    if duration == 0:
        return np.zeros(0)

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Vibrato 参数
    vibrato_rate = 5  # 颤音速率（Hz）
    vibrato_depth = 0.00005  # 颤音深度（相对主频的百分比）

    # 添加 vibrato 到频率上（调频）
    vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)

    # 谐波系数
    # harmonics = [1.0, 0.209, 0.903, 0.141, 0.188, 0.153, 0.044, 0.061, 0.01, 0.057, 0.02, 0.003, 0.006, 0.006, 0.004, 0.009]
    harmonics = [1.0, 0.18, 0.606, 0.039, 0.256, 0.135, 0.047, 0.04, 0.051, 0.048, 0.026, 0.018, 0.014, 0.012, 0.007, 0.008]

    # 合成波形
    waveform = np.zeros_like(t)
    for n, amp in enumerate(harmonics):
        # 调制每个谐波的频率
        modulated_freq = freq * (n + 1) * vibrato
        waveform += amp * np.sin(2 * np.pi * modulated_freq * t)
    waveform /= np.max(np.abs(waveform) + 1e-12)#防止失真
    waveform *= volume

    # 应用ADSR包络
    attack_time = 0.2
    decay_time = 0.1
    sustain_level = 0.8
    release_time = 0.3
    waveform = apply_adsr(waveform, sample_rate, attack_time, decay_time, sustain_level, release_time)

    return waveform
