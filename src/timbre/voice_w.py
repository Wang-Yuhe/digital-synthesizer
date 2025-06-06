# from timbre.adsr import apply_adsr
# import numpy as np

# def voice_w(freq, duration, sample_rate, volume):
#     t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

#     # Vibrato 参数
#     vibrato_rate = 6  # 颤音速率（Hz）
#     vibrato_depth = 0.0001  # 颤音深度（相对主频的百分比）

#     # 添加 vibrato 到频率上（调频）
#     vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)

#     # 谐波系数
#     harmonics = [1.0, 0.239, 0.623, 0.142, 0.041, 0.056, 0.06, 0.047, 0.037, 0.034, 0.033, 0.035, 0.035, 0.035, 0.035, 0.035]

#     # 合成波形
#     waveform = np.zeros_like(t)
#     for n, amp in enumerate(harmonics):
#         # 调制每个谐波的频率
#         modulated_freq = freq * (n + 1) * vibrato
#         waveform += amp * np.sin(2 * np.pi * modulated_freq * t)
#     waveform *= volume

#     # ADSR 包络
#     attack_time = 0.02
#     decay_time = 0.1
#     sustain_level = 0.9
#     release_time = 0.25
#     waveform = apply_adsr(waveform, sample_rate, attack_time, decay_time, sustain_level, release_time)

#     waveform /= np.max(np.abs(waveform)+1e-12)
#     waveform *= volume

#     return waveform
import numpy as np
from scipy.signal import butter, lfilter, iirpeak
from timbre.adsr import apply_adsr

def highpass(data, cutoff, fs, order=3):
    b, a = butter(order, cutoff / (fs / 2), btype='high')
    return lfilter(b, a, data)

def apply_formant_filter(wave, fs, formants):
    for f0 in formants:
        b, a = iirpeak(f0 / (fs / 2), Q=10)
        wave = lfilter(b, a, wave)
    return wave

def add_reverb(waveform, sample_rate, delay_time=0.03, decay=0.3):
    delay = int(delay_time * sample_rate)
    reverb = np.zeros_like(waveform)
    if delay < len(waveform):
        reverb[delay:] = decay * waveform[:-delay]
    return waveform + reverb

def voice_w(freq, duration, sample_rate, volume):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # 更自然 vibrato（速率随时间微变）
    vibrato_rate = 5.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t)
    vibrato_depth = 0.002
    vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)

    # 添加 jitter（周期微抖动）
    jitter = 1 + 0.0015 * np.random.randn(len(t))

    # 谐波结构
    harmonics = [1.0, 0.239, 0.623, 0.142, 0.041, 0.056, 0.06, 0.047,
                 0.037, 0.034, 0.033, 0.035, 0.035, 0.035, 0.035, 0.035]
    waveform = np.zeros_like(t)
    for n, amp in enumerate(harmonics):
        modulated_freq = freq * (n + 1) * vibrato * jitter
        waveform += amp * np.sin(2 * np.pi * modulated_freq * t)

    waveform *= volume

    # 添加 breath noise（高频气息）
    noise = np.random.randn(len(t))
    breath = highpass(noise, 3000, sample_rate) * 0.005
    waveform += breath

    # 应用 ADSR 包络
    waveform = apply_adsr(waveform, sample_rate, 0.03, 0.12, 0.85, 0.3)

    # 应用 formant 共鸣（模拟 [a] 音：F1≈700Hz, F2≈1200Hz）
    waveform = apply_formant_filter(waveform, sample_rate, [700, 1200])

    # 添加简单混响
    waveform = add_reverb(waveform, sample_rate)

    # 归一化
    waveform /= np.max(np.abs(waveform) + 1e-12)
    waveform *= volume

    return waveform
