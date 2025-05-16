import numpy as np
from NoteBlock import NoteBlock
class Track:
    """音轨类"""
    
    def __init__(self, timbre: str, pitch_range: str, bpm: int, sample_rate:int, volume:float, track_id: int):
        #in接口
        self.track_id = track_id
        self.track_name = "Track"+str(track_id)
        self.timbre = timbre  # 音色
        self.pitch_range = pitch_range
        self.volume = volume # 音轨音量比重，音量范围 0-1

        self.note_blocks = []  # List[NoteBlock]

        #out接口
        self.waveform = None 
        
    def add_note_block(self, timre:str, bpm:int, sample_rate:int, volume:float, position: float, note_names , beat_times) -> None:
        """
        添加音块

        :param position: 音块在音轨的位置(下标)
        :param volume: 传给note_block需要计算好比重，传入绝对音量
        :param note_names: List[Note_name]
        :param beat_times: List[int]，每个音符的节拍数
        """
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
