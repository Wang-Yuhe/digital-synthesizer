from timbre.adsr import apply_adsr
import numpy as np

def flute(freq, duration, sample_rate, volume):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # 谐波系数
    harmonics = [1.0, 0.47, 0.25, 0.08, 0.03, 0.015, 0.008, 0.004]
    
    # 合成波形
    waveform = np.zeros_like(t)
    for n, amp in enumerate(harmonics):
        waveform += amp * np.sin(2 * np.pi * freq * (n + 1) * t)
    waveform *= volume

    # 应用ADSR包络
    attack_time = duration * 0.2
    decay_time = duration * 0.1
    sustain_level = 0.8
    release_time = duration * 0.3
    waveform = apply_adsr(waveform, sample_rate, attack_time, decay_time, sustain_level, release_time)

    return waveform
    

    
