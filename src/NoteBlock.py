import numpy as np
from Note import Note
class NoteBlock:
    """音块类"""

    def __init__(self,timre:str, bpm:int, sample_rate:int, volume:float, position:float, note_names, beat_times, block_id: int):
        #in接口
        self.block_id = block_id
        self.timre = timre
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.volume = volume
        self.position = position
        self.note_names = note_names
        self.beat_times = beat_times
        
        self.notes = []  # List[Note]
        
        #out接口
        self.waveform = None  # ndarray
        
    def generate_audio_data(self) -> np.ndarray:
        """生成音频数据"""
        pass

    def set_duration(self, bpm: float = 120, div: int = 4) -> None:
        """根据bpm和音符类型设置时值（单位毫秒），默认为120bpm下的四分音符，即500ms"""
        pass
        
    def add_note(self, timbre: str, bpm:int, sample_rate:int, note_name: str, beat_time: int, volume) -> None:
        """添加音符"""
        pass