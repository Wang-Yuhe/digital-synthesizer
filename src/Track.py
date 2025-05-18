import numpy as np
from NoteBlock import NoteBlock
import sounddevice as sd
class Track:
    """音轨类"""
    
    def __init__(self, timbre: str, pitch_range: str, bpm: int, sample_rate:int, volume:float, track_id: int):
        #in接口
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.timbre = timbre
        self.track_id = track_id
        self.track_name = "Track"+str(track_id)
        self.pitch_range = pitch_range
        self.volume = volume # 音轨音量比重，音量范围 0-1
        self.lowest_note = "C3" 
        self.highest_note = "B5"

        self.note_blocks = []  # List[NoteBlock]

        #out接口
        self.waveform = None 
        
    def add_note_block(self, note_names: list[str], beat_times: list[float], volume: list[float], block_id: int) -> bool:
        """
        添加音块

        :param note_names: List[str]，音块中的包含音符的音名
        :param beat_times: List[int]，每个音符的节拍数
        :param volume: 传给note_block需要计算好比重，传入绝对音量
        :param block_id: 音块在音轨的位置(下标)
        """
        note_block = NoteBlock(self.timbre, self.bpm, self.sample_rate, note_names, beat_times, volume, block_id)
        self.note_blocks.insert(block_id, note_block)
        return True
        
    def remove_note_block(self, block_id: int) -> bool:
        """删除音块"""
        if block_id < 0 or block_id >= len(self.note_blocks):
            return False
        del self.note_blocks[block_id]
        for i in range(len(self.note_blocks)):
            self.note_blocks[i].block_id = i
        return True
        
    def generate_waveform(self) -> np.ndarray:
        """生成音频数据"""
        self.waveform = [note_block.generate_waveform() for note_block in self.note_blocks]
        self.waveform = np.concatenate(self.waveform) * self.volume
        return self.waveform
        
    def calculate_pitch_range(self) -> str:
        """计算音高区间"""
        pass
        
    def change_timbre(self, target_timbre: str) -> bool:
        """改变音色"""
        pass

def play_little_star():
    # 主旋律轨道 (保持不变)
    track = Track("piano", "C3-B5", 120, 44100, 0.5, 0)
    track.add_note_block(["C4"], [1], [0.5], 0)
    track.add_note_block(["C4"], [1], [0.5], 1)
    track.add_note_block(["G4"], [1], [0.5], 2)
    track.add_note_block(["G4"], [1], [0.5], 3)
    track.add_note_block(["A4"], [1], [0.5], 4)
    track.add_note_block(["A4"], [1], [0.5], 5)
    track.add_note_block(["G4"], [2], [0.5], 6)
    track.add_note_block(["F4"], [1], [0.5], 7)
    track.add_note_block(["F4"], [1], [0.5], 8)
    track.add_note_block(["E4"], [1], [0.5], 9)
    track.add_note_block(["E4"], [1], [0.5], 10)
    track.add_note_block(["D4"], [1], [0.5], 11)
    track.add_note_block(["D4"], [1], [0.5], 12)
    track.add_note_block(["C4"], [2], [0.5], 13)
    track.add_note_block(["G4"], [1], [0.5], 14)
    track.add_note_block(["G4"], [1], [0.5], 15)
    track.add_note_block(["F4"], [1], [0.5], 16)
    track.add_note_block(["F4"], [1], [0.5], 17)
    track.add_note_block(["E4"], [1], [0.5], 18)
    track.add_note_block(["E4"], [1], [0.5], 19)
    track.add_note_block(["D4"], [2], [0.5], 20)
    track.add_note_block(["G4"], [1], [0.5], 21)
    track.add_note_block(["G4"], [1], [0.5], 22)
    track.add_note_block(["F4"], [1], [0.5], 23)
    track.add_note_block(["F4"], [1], [0.5], 24)
    track.add_note_block(["E4"], [1], [0.5], 25)
    track.add_note_block(["E4"], [1], [0.5], 26)
    track.add_note_block(["D4"], [2], [0.5], 27)
    track.add_note_block(["C4"], [1], [0.5], 28)
    track.add_note_block(["C4"], [1], [0.5], 29)
    track.add_note_block(["G4"], [1], [0.5], 30)
    track.add_note_block(["G4"], [1], [0.5], 31)
    track.add_note_block(["A4"], [1], [0.5], 32)
    track.add_note_block(["A4"], [1], [0.5], 33)
    track.add_note_block(["G4"], [2], [0.5], 34)
    track.add_note_block(["F4"], [1], [0.5], 35)
    track.add_note_block(["F4"], [1], [0.5], 36)
    track.add_note_block(["E4"], [1], [0.5], 37)
    track.add_note_block(["E4"], [1], [0.5], 38)
    track.add_note_block(["D4"], [1], [0.5], 39)
    track.add_note_block(["D4"], [1], [0.5], 40)
    track.add_note_block(["C4"], [2], [0.5], 41)
    track.generate_waveform()
    sd.play(track.waveform, samplerate=track.sample_rate)
    sd.wait()
if __name__ == "__main__":
    play_little_star()
    