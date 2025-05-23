import numpy as np
from timbre.adsr import apply_adsr
import sounddevice as sd#到时候可以删去
from scipy.signal import butter, lfilter

def harp(freq, duration, sample_rate, volume):
    harmonics = [1.0, 0.555, 0.016, 0.025, 0.691, 0.011, 0.006, 0.039, 0.008, 0.012, 0.022, 0.028, 0.015, 0.005, 0.015, 0.011]
    waveform=timbre_synthesis(freq, duration, sample_rate, volume, harmonics, 0.006, 0.034, 0.3, 0.836)
    return waveform

def lowpass_filter(waveform, N, wc, sample_rate):#wc截止频率,butter平稳的滤波器
    b,a = butter(N, wc/(sample_rate*0.5))#scipy 的滤波器设计函数要求频率是相对于 奈奎斯特频率（Nyquist = sample_rate / 2）的比例
    return lfilter(b, a, waveform)

def lfo(freq, lfo_rate, lfo_depth, t):
    """
    lfo = np.sin(2 * np.pi * lfo_rate * t)
    freq = freq + lfo_depth*lfo
    return freq
    """
    return t + (lfo_depth / (2*np.pi*lfo_rate)) * (1-np.cos(2*np.pi*lfo_rate*t))#周期性时移

def timbre_synthesis(freq, duration, sample_rate, volume, harmonics, 
                       attack_rate, decay_rate, sustain_level, release_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    phase_integral = lfo(freq, 5, 0.001, t)#lfo调制，模拟琴弦波动
    #freq = lfo(freq, 8, 0.01, t)

    #增加谐波成分(决定音色)，基波+若干谐波(振幅递减，频率整数倍)
    waveform = sum(amplitude * np.sin(2 * np.pi * freq * (i + 1) * phase_integral)
            for i, amplitude in enumerate(harmonics))
    waveform /= np.max(np.abs(waveform) + 1e-12)#防止失真
    waveform *= volume

    #增加adsr包络，使振幅更自然
    waveform=apply_adsr(waveform,sample_rate,duration*attack_rate,duration*decay_rate, sustain_level, duration*release_rate)
    #waveform=waveform*(t**0.01*np.exp(-3*t))
    #waveform=lowpass_filter(waveform, 4, 3500, sample_rate)
    waveform *= np.exp(-2 * t)#模拟空气阻力

    #wavfile.write('generated_audio.wav', self.sample_rate, self.waveform.astype(np.float32))
    #sd.play(waveform, samplerate=sample_rate)#在线播放
    #sd.wait()
    return waveform