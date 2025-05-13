import numpy as np
from NoteBlock import NoteBlock
class Track:
    """音轨类"""
    
    def __init__(self, track_id: int):
        self.track_id = track_id
        self.track_name = "Track 1"
        self.timbre = "piano"  # 默认音色
        self.pitch_range = "C4-C6"
        self.note_blocks = []  # List[NoteBlock]
        self.waveform = None 
        self.volume = 1 # 音轨音量，音量范围 0-1
        
    def add_note_block(self, position: float, note_block: NoteBlock, duration: int) -> None:
        """添加音块"""
        pass
        
    def remove_note_block(self, position: float) -> bool:
        """删除音块"""
        pass
        
    def generate_audio_data(self) -> np.ndarray:
        """生成音频数据"""
        pass
        
    def calculate_pitch_range(self) -> str:
        """计算音高区间"""
        pass
        
    def change_timbre(self, target_timbre: str) -> bool:
        """改变音色"""
        pass
