import numpy as np
class Note:
    """音符类"""
    
    def __init__(self, note_name: int):
        #修改初始化方式，note_name输入格式为:音名(C,C#...B)+数字(0~8)
        self.note_id = 1
        self.note_name = note_name
        self.duration = 60
        self.volume = 1 # 音量范围 0-1
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

    def generate_audio_data(self) -> np.ndarray:
        """生成音频数据"""
        pass
