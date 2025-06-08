"""竖琴音色"""
import numpy as np
from src.timbre.adsr import apply_adsr
from src.timbre.filter import lowpass_filter
from src.timbre.oscillator import oscillator

def harp(freq, duration, sample_rate, volume):
    """竖琴音色"""
    harmonics = [1.0, 0.555, 0.016, 0.025, 0.691, 0.011, 0.006, 0.039, 0.008, 0.012, 0.022, 0.028, 0.015, 0.005, 0.015, 0.011]
    waveform=timbre_synthesis(freq, duration, sample_rate, volume, harmonics)
    return waveform

def lfo(lfo_rate, lfo_depth, t):
    """低频振荡器"""
    # lfo = np.sin(2 * np.pi * lfo_rate * t)
    # freq = freq + lfo_depth*lfo
    # return freq
    return t + (lfo_depth / (2*np.pi*lfo_rate)) * (1-np.cos(2*np.pi*lfo_rate*t))#周期性时移

def timbre_synthesis(freq, duration, sample_rate, volume, harmonics):
    """根据不同的音高（时域频率）合成音色"""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    lfo_t = lfo(5, 0.001, t)#lfo调制，模拟琴弦波动
    #freq = lfo(freq, 8, 0.01, t)

    B=0.001#弦的刚性
    decays = np.linspace(3.0, 6.0, len(harmonics))#高次泛音衰减的更快,不同谐波衰减速度不同,独立包络

    #增加谐波成分(决定音色)，基波+若干谐波(振幅递减，频率整数倍)
    waveform=np.zeros_like(t)
    for i, amplitude in enumerate(harmonics):
        amp_freq = freq*(i+1) * np.sqrt(1+B*(i+1)**2)#现实中的弦不会产生完美的谐波（非谐波性）
        #amp_freq = lfo(freq*(i+1), 5*(i+1)/10, 0.007, t)
        #amp_freq = freq*(i+1) * (1 + (np.random.rand()-0.5)*DETUNE*0.001)
        #waveform += amplitude*np.exp(-decays[i]*lfo_t) * np.sin(2*np.pi*amp_freq*lfo_t)
        waveform += amplitude*np.exp(-decays[i]*lfo_t) * oscillator('sine', amp_freq, lfo_t)

    #增加adsr包络，使振幅更自然
    waveform=apply_adsr(waveform,sample_rate,0.005,0.05, 0.4, 0.7)
    #waveform=waveform*(t**0.01*np.exp(-3*t))
    waveform *= np.exp(-2 * lfo_t)#模拟空气阻力

    waveform =lowpass_filter(waveform, 3500, 4, sample_rate)

    waveform /= np.max(np.abs(waveform) + 1e-12)#防止失真
    waveform *= volume

    #wavfile.write('generated_audio.wav', self.sample_rate, self.waveform.astype(np.float32))
    #sd.play(waveform, samplerate=sample_rate)#在线播放
    #sd.wait()
    return waveform
