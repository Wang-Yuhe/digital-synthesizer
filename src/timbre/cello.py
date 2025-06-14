"""大提琴音色"""
import numpy as np

from src.timbre.adsr import apply_adsr

def rms_normalize(waveform):
    """使用RMS归一化波形"""
    rms = np.sqrt(np.mean(waveform**2))
    if rms > 0:
        return waveform / rms
    return waveform

def cello(freq, duration, sample_rate, volume):
    """
    大提琴音色

    Args:
        freq (float): 频率
        duration (float): 时值，表示单音的持续时间
        sample_rate (float): 采样率
        volume (float): 音量大小，0~1的范围
    
    Returns:
        waveform (np.ndarray): 合成大提琴音色后的波形
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # 调整谐波成分
    harmonics = [1.0, 0.5, 0.3, 0.2]  # 增加高频成分以增加粗糙感
    waveform = sum(volume * amplitude * np.sin(2 * np.pi * freq * (i + 1) * t)
                        for i, amplitude in enumerate(harmonics))

    # 增加低频噪声以增强低频特性
    noise_amplitude = 0.25  # 适度增加噪声幅度
    noise = np.random.normal(0, noise_amplitude, len(t))

    # 低通滤波器：使用简单的移动平均来增强低频噪声
    window_size = 120  # 调整窗口大小以平衡低频和粗糙感
    low_pass_noise = np.convolve(noise, np.ones(window_size) / window_size, mode='same')

    waveform += low_pass_noise

    # 增加颤音效果以增加不稳定性
    vibrato_depth = 0.04
    vibrato_rate = 10
    vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
    waveform *= vibrato

    # 归一化
    waveform /= np.max(np.abs(waveform))

    # 增加非线性失真以增加粗糙感
    waveform = np.tanh(2.0 * waveform)

    # 应用ADSR包络
    attack_time = duration * 0.05
    decay_time = duration * 0.1
    sustain_level = 0.6
    release_time = duration * 0.85
    apply_adsr(waveform,sample_rate,attack_time, decay_time, sustain_level, release_time)

    return rms_normalize(waveform)
