from timbre.adsr import apply_adsr
import numpy as np

def flute(freq, duration, sample_rate, volume):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Vibrato 参数
    vibrato_rate = 5  # 颤音速率（Hz）
    vibrato_depth = 0.00005  # 颤音深度（相对主频的百分比）

    # 添加 vibrato 到频率上（调频）
    vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)

    # 谐波系数
    harmonics = [1.0, 0.209, 0.903, 0.141, 0.188, 0.153, 0.044, 0.061, 0.01, 0.057, 0.02, 0.003, 0.006, 0.006, 0.004, 0.009]
    
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
    

    
