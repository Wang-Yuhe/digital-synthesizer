import numpy as np
import scipy.io.wavfile as wavfile
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.signal as sg

class Note:
    """音符类"""
    
    def __init__(self,timbre:str, bpm:int, sample_rate:int, note_name, beat_time, volume, note_id):
        #修改初始化方式，note_name输入格式为:音名(C,C#...B)+数字(0~8)
        #in接口
        self.note_id = note_id
        self.note_name = note_name
        self.beat_time = beat_time#节拍数
        self.volume = volume # 音量范围 0-1
        self.timbre = timbre

        self.duration = beat_time/bpm*60
        self.sample_rate = sample_rate

        #out接口
        self.waveform = None  # ndarray
    
    def note2freq(self, note):#音符转频率,note格式为C4
        #C,C#,D,D#,E,F,F#,G,G#,A,A#,B
        note_map = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
                'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        for k in sorted(note_map.keys(), key=lambda x: -len(x)):
            if note.startswith(k):
                octave = int(note[len(k):])
                midi_num = 12 * (octave + 1) + note_map[k]
                return 440.0 * (2 ** ((midi_num - 69) / 12))
                
        raise ValueError("Invalid note format")

    def generate_waveform(self) -> np.ndarray:
        freq=self.note2freq(self.note_name)
        if self.timbre == "piano":
            t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
            
            #增加谐波成分(决定音色)，基波+若干谐波(振幅递减，频率整数倍)
            harmonics = [1,0.340,0.102,0.085,0.070,0.065,0.028,0.010,0.014,0.012,0.013,0.004]
            self.waveform = sum(self.volume * amplitude * np.sin(2 * np.pi * freq * (i + 1) * t)
                   for i, amplitude in enumerate(harmonics))
            self.waveform /= np.max(np.abs(self.waveform))

            #增加adsr包络，使振幅更自然
            self.apply_adsr(self.duration*0.01,self.duration*0.03,0.4,self.duration*0.8)
            #self.waveform=self.waveform*(t**0.01*np.exp(-3*t))

            #wavfile.write('generated_audio.wav', self.sample_rate, self.waveform.astype(np.float32))
            sd.play(self.waveform, samplerate=self.sample_rate)#在线播放
            sd.wait()
        return self.waveform

    def show_time_and_freq_domain(self):
        t = np.linspace(0, self.duration, len(self.waveform), endpoint=False)

        # -------- 时域图 --------
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(t, self.waveform)
        plt.title(f"Time Domain: {self.note_name} ({self.timbre})")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)

        # -------- 频域图 --------
        N = len(self.waveform)
        freq_domain = np.fft.fft(self.waveform)
        freq = np.fft.fftfreq(N, d=1/self.sample_rate)

        # 取正频率部分
        half_N = N // 2
        magnitude = np.abs(freq_domain[:half_N])
        magnitude /= np.max(magnitude)  # 归一化
        freq = freq[:half_N]

        plt.subplot(1, 2, 2)
        plt.plot(freq, magnitude)#转换成分贝
        plt.title("Frequency Domain")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Normalized Amplitude")
        plt.grid(True)

        plt.tight_layout()
        plt.show()


    def apply_adsr(self,attack_time=0.01, decay_time=0.1,sustain_level=0.8, release_time=0.2):
        """增加adsr包络曲线"""
        total_samples = len(self.waveform)
        
        attack_samples = int(self.sample_rate * attack_time)
        decay_samples = int(self.sample_rate * decay_time)
        release_samples = int(self.sample_rate * release_time)
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
        
        self.waveform*=envelope


    def generate_audio_data(self) -> np.ndarray:
        """生成音频数据"""
        pass

if __name__=="__main__":
    note=Note("piano",60,44100,"E4",2,0.5,0)
    note.generate_waveform()