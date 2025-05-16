import numpy as np
import scipy.io.wavfile as wavfile

class Note:
    """音符类"""
    
    def __init__(self,timbre:str, bpm:int, sample_rate:int, note_id, note_name, beat_time, volume):
        #修改初始化方式，note_name输入格式为:音名(C,C#...B)+数字(0~8)
        #in接口
        self.note_id = note_id
        self.note_name = note_name
        self.beat_time = beat_time#节拍数
        self.volume = volume # 音量范围 0-1

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

    def generate_waveform(self):
        freq=self.note2freq(self.note_name)
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        self.waveform = self.volume * np.sin(2 * np.pi * freq * t)

        wavfile.write('generated_audio.wav', self.sample_rate, self.waveform.astype(np.float32))


    def generate_audio_data(self) -> np.ndarray:
        """生成音频数据"""
        pass

if __name__=="__main__":
    note=Note(1,"G",1,0.5)
    note.generate_waveform()