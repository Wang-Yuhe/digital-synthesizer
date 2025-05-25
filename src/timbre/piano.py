import numpy as np
from timbre.adsr import apply_adsr
from timbre.filter import lowpass_filter,band_filter
import sounddevice as sd#到时候可以删去
from scipy.signal import butter, lfilter

def lfo(freq, lfo_rate, lfo_depth, t):
    lfo = np.sin(2 * np.pi * lfo_rate * t)
    freq = freq + lfo_depth*lfo
    return freq
    #return t + (lfo_depth / (2*np.pi*lfo_rate)) * (1-np.cos(2*np.pi*lfo_rate*t))#周期性时移

def piano(freq, duration, sample_rate, volume):
    #harmonics = [1.0, 0.144, 0.107, 0.165, 0.059, 0.122, 0.136, 0.26, 0.245, 0.653, 0.02, 0.18, 0.064, 0.121, 0.014, 0.028]
    #harmonics = [1.0, 0.629, 0.078, 0.089, 0.005, 0.159, 0.008, 0.011, 0.014, 0.004, 0.002, 0.001, 0.001, 0.001, 0.001]
    harmonics = [1.0, 0.778, 0.019, 0.085, 0.023, 0.034, 0.065, 0.023, 0.031, 0.015, 0.009, 0.019, 0.053, 0.018, 0.052, 0.004]

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    B=0.0004#金属弦的刚性
    DETUNE=0.999
    #对谐波成分做分析发现，不同频率的谐波成分也是不同的
    if freq<250: decays = np.linspace(1.2, 2.5, len(harmonics))#高次泛音衰减的更快,不同谐波衰减速度不同,独立包络
    elif freq<2000: decays = np.linspace(2.5, 5.0, len(harmonics))
    else: decays = np.linspace(4, 5.5, len(harmonics))

    #增加谐波成分(决定音色)，基波+若干谐波(振幅递减，频率整数倍)
    waveform=np.zeros_like(t)
    for i, amplitude in enumerate(harmonics):
        amp_freq = freq*(i+1) * np.sqrt(1+B*(i+1)**2)#现实中的弦不会产生完美的谐波（非谐波性）
        #amp_freq = lfo(freq*(i+1), 5*(i+1)/10, 0.007, t)
        #amp_freq = freq*(i+1) * (1 + (np.random.rand()-0.5)*DETUNE*0.001)
        waveform += amplitude*np.exp(-decays[i]*t) * np.sin(2*np.pi*amp_freq*t)

    noise = np.random.randn(len(t))
    attack_time = 0.02 
    noise_decay = np.linspace(1,0, int(attack_time*sample_rate))
    noise_decay = np.pad(noise_decay, (0, len(t)-len(noise_decay)), mode='constant')*0.2#白噪音包络线
    waveform += noise * noise_decay*volume#增加敲键的白噪音

    #增加adsr包络，使振幅更自然
    waveform=apply_adsr(waveform,sample_rate, 0.01, 0.2, 0.5, duration*0.2)
    #waveform=waveform*(t**0.01*np.exp(-3*t))

    waveform=lowpass_filter(waveform,  4000, 4, sample_rate)#动态调整截止频率

    waveform /= np.max(np.abs(waveform)+1e-12)
    waveform *= volume

    #wavfile.write('generated_audio.wav', self.sample_rate, self.waveform.astype(np.float32))
    #sd.play(waveform, samplerate=sample_rate)#在线播放
    #sd.wait()
    return waveform
