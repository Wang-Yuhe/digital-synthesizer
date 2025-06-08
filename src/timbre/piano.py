"""钢琴音色"""
import numpy as np
from src.timbre.adsr import apply_adsr
from src.timbre.filter import lowpass_filter
from src.timbre.oscillator import oscillator

def lfo(freq, lfo_rate, lfo_depth, t):
    """低频振荡器"""
    lfos = np.sin(2 * np.pi * lfo_rate * t)
    freq = freq + lfo_depth * lfos
    return freq
    # return t + (lfo_depth / (2*np.pi*lfo_rate)) * (1-np.cos(2*np.pi*lfo_rate*t))#周期性时移

def piano(freq, duration, sample_rate, volume):
    """钢琴音色"""
    # harmonics = [1.0, 0.144, 0.107, 0.165, 0.059, 0.122, 0.136, 0.26, 0.245, 0.653, 0.02, 0.18, 0.064, 0.121, 0.014, 0.028]
    # harmonics = [1.0, 0.778, 0.019, 0.085, 0.023, 0.034, 0.065, 0.023, 0.031, 0.015, 0.009, 0.019, 0.053, 0.018, 0.052, 0.004]
    harmonics = [1.0, 0.8806691627639035, 0.12006790037144367, 0.14348630114711755,
                 0.11335373778517048, 0.07498546962916296, 0.12858452920377123,
                 0.07015291983917817, 0.013380413377920999, 0.024781539462613484,
                 0.012414402853577039, 0.034155326189328775, 0.035865879813986555,
                 0.02133029278893286, 0.008390883093868564, 0.007886337830904378]

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    B=0.0004#金属弦的刚性
    # DETUNE=0.999
    # 对谐波成分做分析发现，不同频率的谐波成分也是不同的
    decays = np.linspace(2.5, 5.0, len(harmonics)) / duration / 2#高次泛音衰减的更快,不同谐波衰减速度不同,独立包络

    # 增加谐波成分(决定音色)，基波+若干谐波(振幅递减，频率整数倍)
    waveform=np.zeros_like(t)
    for i, amplitude in enumerate(harmonics):
        amp_freq = freq*(i+1) * np.sqrt(1+B*(i+1)**2)#现实中的弦不会产生完美的谐波（非谐波性）
        # amp_freq = lfo(freq*(i+1), 5*(i+1)/10, 0.007, t)
        # amp_freq = freq*(i+1) * (1 + (np.random.rand()-0.5)*DETUNE*0.001)
        # waveform += amplitude*np.exp(-decays[i]*t) * np.sin(2*np.pi*amp_freq*t)
        waveform += amplitude*np.exp(-decays[i]*t) * oscillator('sine', amp_freq, t)

    noise = np.random.randn(len(t))
    attack_time = 0.02
    noise_decay = np.linspace(1,0, int(attack_time*sample_rate))
    noise_decay = np.pad(noise_decay, (0, len(t)-len(noise_decay)), mode='constant')*0.2 # 白噪音包络线
    waveform += noise * noise_decay*volume # 增加敲键的白噪音

    # 增加adsr包络，使振幅更自然
    waveform=apply_adsr(waveform,sample_rate, 0.01, 0.2, 0.5, 0.2)
    # waveform=waveform*(t**0.01*np.exp(-3*t))

    waveform=lowpass_filter(waveform,  4000, 4, sample_rate) # 动态调整截止频率

    waveform /= np.max(np.abs(waveform)+1e-12)
    waveform *= volume

    # wavfile.write('generated_audio.wav', self.sample_rate, self.waveform.astype(np.float32))
    # sd.play(waveform, samplerate=sample_rate)#在线播放
    # sd.wait()
    return waveform
