import numpy as np

def apply_adsr(waveform, sample_rate=44100, attack_time=0.01, decay_time=0.1,sustain_level=0.8, release_time=0.2):
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
    sustain_env = np.full(sustain_samples, sustain_level)#保持不变
    release_env = np.linspace(sustain_level, 0, release_samples)
    
    envelope = np.concatenate([attack_env, decay_env, sustain_env, release_env])
    
    # 截断或填补以匹配 wave 长度
    if len(envelope) > total_samples:
        envelope = envelope[:total_samples]
    else:
        envelope = np.pad(envelope, (0, total_samples - len(envelope)))
    
    waveform*=envelope
    return waveform