import numpy as np
from timbre.filter import lowpass_filter,band_filter
from timbre.oscillator import oscillator
from scipy.signal import butter, lfilter


def rms_normalize(waveform):
    """使用RMS归一化波形"""
    rms = np.sqrt(np.mean(waveform**2))
    if rms > 0:
        return waveform / rms
    return waveform

def apply_adsr(waveform,sample_rate,attack_time=0.01, decay_time=0.1, sustain_level=0.8, release_time=0.2):
    """增加adsr包络曲线"""
    total_samples = len(waveform)

    attack_samples = int(sample_rate * attack_time)
    decay_samples = int(sample_rate * decay_time)
    release_samples = int(sample_rate * release_time)
    sustain_samples = total_samples - (attack_samples + decay_samples + release_samples)
    sustain_samples = max(sustain_samples, 0)

    # 各阶段的包络
    attack_env = np.linspace(0, 1, attack_samples)
    decay_env = np.linspace(1, sustain_level, decay_samples)
    sustain_env = np.full(sustain_samples, sustain_level)  # 保持不变
    release_env = np.linspace(sustain_level, 0, release_samples)

    envelope = np.concatenate([attack_env, decay_env, sustain_env, release_env])

    # 截断或填补以匹配 wave 长度
    if len(envelope) > total_samples:
        envelope = envelope[:total_samples]
    else:
        envelope = np.pad(envelope, (0, total_samples - len(envelope)))

    waveform *= envelope

def violin(freq, duration, sample_rate, volume):
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
