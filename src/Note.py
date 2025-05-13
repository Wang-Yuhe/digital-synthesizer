import numpy as np
class Note:
    """音符类"""
    
    def __init__(self, note_id: int):
        self.note_id = note_id
        self.note_name = "C4"
        self.duration = 60
        self.volume = 1 # 音量范围 0-1
        self.waveform = None  # ndarray
        
    def generate_audio_data(self) -> np.ndarray:
        """生成音频数据"""
        pass