import numpy as np
import scipy.io.wavfile as wavfile
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.signal as sg

from timbre.piano import piano
from timbre.harp import harp
from timbre.flute import flute

class Note:
    """音符类"""
    
    def __init__(self, timbre: str = "piano", bpm: int = 120, sample_rate: int = 44100, 
                 note_name: str = "C4", beat_time: float = 1.0, volume: float = 1.0, note_id: int = 0):
        #修改初始化方式，note_name输入格式为:音名(C,C#,Db...B)+数字(0~8)/rest(休止符)
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
    
    def note_midi(self):
        if self.note_name.lower() == 'rest':
            raise ValueError("Cannot compare rest note.")
        note_map = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5,
            'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
        for k in sorted(note_map.keys(), key=lambda x: -len(x)):
            if self.note_name.startswith(k):
                octave = int(self.note_name[len(k):])
                return 12 * octave + note_map[k]
        raise ValueError("Invalid note format")

    def __lt__(self, other):
        """
        比较两个音高的大小(禁止与休止符比较)
        """
        return self.note_midi()<other.note_midi()

    def __gt__(self, other):
        return self.note_midi()>other.note_midi()

    def __eq__(self, other):
        return self.note_midi()==other.note_midi()

    def note2freq(self, note):#音符转频率,note格式为C4
        #C,C#,D,D#,E,F,F#,G,G#,A,A#,B
        if note=="rest": return 0
        note_map = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5,
                'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
        for k in sorted(note_map.keys(), key=lambda x: -len(x)):
            if note.startswith(k):
                octave = int(note[len(k):])
                midi_num = 12 * (octave + 1) + note_map[k]
                return 440.0 * (2 ** ((midi_num - 69) / 12))
                
        raise ValueError("Invalid note format")

    def generate_waveform(self) -> np.ndarray:
        freq=self.note2freq(self.note_name)
        if freq==0:
            self.waveform = np.zeros(int(self.sample_rate * self.duration))
            return self.waveform
        if self.timbre == "piano":
            self.waveform=piano(freq, self.duration, self.sample_rate, self.volume)
        elif self.timbre == "harp":
            self.waveform=harp(freq, self.duration, self.sample_rate, self.volume)
        elif self.timbre == "flute":
            self.waveform=flute(freq, self.duration, self.sample_rate, self.volume)
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

if __name__=="__main__":
    note1=Note("flute",60,44100,"C4",2,1,0)
    #note2=Note("piano",60,44100,"Db4",2,0.5,0)
    note1.generate_waveform()
    #note1.show_time_and_freq_domain()