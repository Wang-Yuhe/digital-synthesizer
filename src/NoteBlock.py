import numpy as np
from Note import Note
from config import BPM
class NoteBlock:
    """音块类"""

    def __init__(self, block_id: int):
        self.block_id = block_id
        self.note_name = "C4"
        self.duration = 500 # 默认一个音块的时值是
        self.notes = []  # List[Note]
        self.waveform = None  # ndarray
        
    def generate_audio_data(self) -> np.ndarray:
        """生成音频数据"""
        pass

    def set_duration(self, duration: float) -> None:
        """设置时值（单位毫秒）"""
        pass

    def set_duration(self, bpm: float = 120, div: int = 4) -> None:
        """根据bpm和音符类型设置时值（单位毫秒），默认为120bpm下的四分音符，即500ms"""
        pass
        
    def add_note(self, note: Note) -> None:
        """添加音符"""
        pass