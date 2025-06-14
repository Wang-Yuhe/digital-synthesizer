"""实现adsr包络曲线"""
import numpy as np

def apply_adsr(waveform, sample_rate=44100, attack_time=0.01, decay_time=0.1,sustain_level=0.8, release_time=0.2):
    """
    为输入的波形添加 ADSR 包络曲线（Attack-Decay-Sustain-Release）。

    参数：
        waveform (np.ndarray): 原始音频波形。
        sample_rate (int): 音频采样率，默认 44100 Hz。
        attack_time (float): 起音阶段持续时间（单位：秒），从 0 上升到最大幅度。
        decay_time (float): 衰减阶段持续时间，从最大幅度下降到保持电平。
        sustain_level (float): 保持阶段的音量电平（0~1），音符按住期间的稳定音量。
        release_time (float): 释放阶段持续时间，从保持电平降至 0。

    返回：
        np.ndarray: 添加了 ADSR 包络的波形。
    """
    total_samples = len(waveform)

    attack_samples = int(sample_rate * attack_time)
    decay_samples = int(sample_rate * decay_time)
    release_samples = int(sample_rate * release_time)
    sustain_samples = total_samples - (attack_samples + decay_samples + release_samples)
    sustain_samples = max(sustain_samples, 0)

    # 各阶段的包络
    attack_env = np.linspace(0, 1, attack_samples)
    decay_env = np.linspace(1, sustain_level, decay_samples)
    sustain_env = np.full(sustain_samples, sustain_level) # 保持不变
    release_env = np.linspace(sustain_level, 0, release_samples)

    envelope = np.concatenate([attack_env, decay_env, sustain_env, release_env])

    # 截断或填补以匹配 wave 长度
    if len(envelope) > total_samples:
        envelope = envelope[:total_samples]
    else:
        envelope = np.pad(envelope, (0, total_samples - len(envelope)))

    waveform*=envelope
    return waveform
