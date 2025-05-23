import numpy as np
from timbre.adsr import apply_adsr
import sounddevice as sd#到时候可以删去
from scipy.signal import butter, lfilter

def lowpass_filter(waveform, N, wc, sample_rate):#wc截止频率,butter平稳的滤波器
    b,a = butter(N, wc/(sample_rate*0.5))#scipy 的滤波器设计函数要求频率是相对于 奈奎斯特频率（Nyquist = sample_rate / 2）的比例
    return lfilter(b, a, waveform)

def lfo(freq, lfo_rate, lfo_depth, t):
    lfo = np.sin(2 * np.pi * lfo_rate * t)
    freq = freq + lfo_depth*lfo
    return freq
    #return t + (lfo_depth / (2*np.pi*lfo_rate)) * (1-np.cos(2*np.pi*lfo_rate*t))#周期性时移

def piano(freq, duration, sample_rate, volume):
    harmonics = [1.0, 0.144, 0.107, 0.165, 0.059, 0.122, 0.136, 0.26, 0.245, 0.653, 0.02, 0.18, 0.064, 0.121, 0.014, 0.028]
    #waveform=timbre_synthesis(freq, duration, sample_rate, volume, harmonics, 0.01, 0.03, 0.4, 0.8)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    freq=lfo(freq, 5, 0.007, t)

    #增加谐波成分(决定音色)，基波+若干谐波(振幅递减，频率整数倍)
    waveform = sum(amplitude * np.sin(2 * np.pi * freq * (i + 1) * t)
            for i, amplitude in enumerate(harmonics))
    waveform /= np.max(np.abs(waveform)+1e-12)
    waveform *= volume

    #增加adsr包络，使振幅更自然
    waveform=apply_adsr(waveform,sample_rate, duration*0.0147, duration*0.0325, 0.4, duration*0.810)
    #waveform=waveform*(t**0.01*np.exp(-3*t))
    waveform=lowpass_filter(waveform, 4, 1500, sample_rate)

    #wavfile.write('generated_audio.wav', self.sample_rate, self.waveform.astype(np.float32))
    #sd.play(waveform, samplerate=sample_rate)#在线播放
    #sd.wait()
    return waveform
