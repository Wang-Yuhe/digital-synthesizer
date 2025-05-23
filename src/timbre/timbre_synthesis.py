import numpy as np
from timbre.adsr import apply_adsr

def timbre_synthesis(freq, duration, sample_rate, volume, harmonics, 
                       attack_rate, decay_rate, sustain_level, release_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    #增加谐波成分(决定音色)，基波+若干谐波(振幅递减，频率整数倍)
    waveform = sum(volume * amplitude * np.sin(2 * np.pi * freq * (i + 1) * t)
            for i, amplitude in enumerate(harmonics))
    #waveform /= np.max(np.abs(waveform))

    #增加adsr包络，使振幅更自然
    waveform=apply_adsr(waveform,sample_rate,duration*attack_rate,duration*decay_rate, sustain_level, duration*release_rate)
    #self.waveform=self.waveform*(t**0.01*np.exp(-3*t))

    #wavfile.write('generated_audio.wav', self.sample_rate, self.waveform.astype(np.float32))
    #sd.play(self.waveform, samplerate=self.sample_rate)#在线播放
    #sd.wait()
    return waveform