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

def double_bass(freq, duration, sample_rate, volume):
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
