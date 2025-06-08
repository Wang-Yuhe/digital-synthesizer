"""音轨类"""
import numpy as np
import sounddevice as sd

from src.note_block import NoteBlock
class Track:
    """音轨类"""

    def __init__(self, timbre: str = "piano", pitch_range: str = "C3-B5", bpm: int = 120,
                 sample_rate:int = 44100, volume: float = 1, track_id: int = 0):
        #in接口
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.timbre = timbre
        self.track_id = track_id
        self.track_name = "Track"+str(track_id)
        self.pitch_range = pitch_range
        self.volume = volume # 音轨音量比重，音量范围 0-1
        self.lowest_note = None
        self.highest_note = None

        self.note_blocks = []  # List[NoteBlock]

        #out接口
        self.waveform = None

    def add_note_block(self, note_names: list[str], beat_times: list[float], volume: list[float] = None,
                    start_beat: list[float] = None, block_id: int = -1) -> bool:
        """
        添加一个音块到音轨中。

        Args:
            note_names (list[str]): 音块中每个音符的名称，例如 ["C4", "E4", "G4"]。
            beat_times (list[float]): 每个音符的节拍数，例如 [1.0, 1.0, 2.0]。
            volume (list[float], optional): 每个音符的音量（绝对值），长度不足时默认补 1。
            start_beat (list[float], optional): 每个音符的起始节拍，长度不足时默认补 0。
            block_id (int, optional): 音块在音轨中的插入位置，默认为 -1 表示追加到末尾。

        Returns:
            bool: 添加成功时返回 True。
        """
        if volume is None:
            volume = []
        if start_beat is None:
            start_beat = []

        if block_id == -1:
            block_id = len(self.note_blocks)
        if len(volume) < len(note_names):
            volume += [1] * (len(note_names) - len(volume))
        if len(start_beat) < len(note_names):
            start_beat += [0] * (len(note_names) - len(start_beat))

        note_block = NoteBlock(timbre=self.timbre, bpm=self.bpm, sample_rate=self.sample_rate,
                            note_names=note_names, beat_times=beat_times, start_beat=start_beat,
                            volume=volume, block_id=block_id)
        self.note_blocks.insert(block_id, note_block)

        for note in note_block.notes:
            if note.note_name == "rest":
                continue
            if self.lowest_note is None or note < self.lowest_note:
                self.lowest_note = note
            if self.highest_note is None or note > self.highest_note:
                self.highest_note = note

        return True


    def remove_note_block(self, block_id: int) -> bool:
        """删除音块"""
        if block_id < 0 or block_id >= len(self.note_blocks):
            return False
        del self.note_blocks[block_id]
        for i, note_block in enumerate(self.note_blocks):
            note_block.block_id = i
        return True

    def generate_waveform(self) -> np.ndarray:
        """生成音频数据"""
        self.waveform = [note_block.generate_waveform() for note_block in self.note_blocks]
        self.waveform = np.concatenate(self.waveform) * self.volume
        return self.waveform

    def calculate_pitch_range(self) -> str:
        """计算音高区间"""
        if self.lowest_note is None or self.highest_note is None:
            self.pitch_range = "No notes in track"
        else:
            self.pitch_range = f"{self.lowest_note.note_name}-{self.highest_note.note_name}"
        return self.pitch_range

    def change_timbre(self, target_timbre: str) -> bool:
        """改变音色"""

def play_little_star():
    """用以临时测试，演奏小星星"""
    # 主旋律轨道 (保持不变)
    track = Track("piano", "C3-B5", 120, 44100, 0.5, 0)
    track.add_note_block(["C4"], [1], [0.5])
    track.add_note_block(["C4"], [1], [0.5])
    track.add_note_block(["G4"], [1], [0.5])
    track.add_note_block(["G4"], [1], [0.5])
    track.add_note_block(["A4"], [1], [0.5])
    track.add_note_block(["A4"], [1], [0.5])
    track.add_note_block(["G4"], [2], [0.5])
    track.add_note_block(["F4"], [1], [0.5])
    track.add_note_block(["F4"], [1], [0.5])
    track.add_note_block(["E4"], [1], [0.5])
    track.add_note_block(["E4"], [1], [0.5])
    track.add_note_block(["D4"], [1], [0.5])
    track.add_note_block(["D4"], [1], [0.5])
    track.add_note_block(["C4"], [2], [0.5])
    track.add_note_block(["G4"], [1], [0.5])
    track.add_note_block(["G4"], [1], [0.5])
    track.add_note_block(["F4"], [1], [0.5])
    track.add_note_block(["F4"], [1], [0.5])
    track.add_note_block(["E4"], [1], [0.5])
    track.add_note_block(["E4"], [1], [0.5])
    track.add_note_block(["D4"], [2], [0.5])
    track.add_note_block(["G4"], [1], [0.5])
    track.add_note_block(["G4"], [1], [0.5])
    track.add_note_block(["F4"], [1], [0.5])
    track.add_note_block(["F4"], [1], [0.5])
    track.add_note_block(["E4"], [1], [0.5])
    track.add_note_block(["E4"], [1], [0.5])
    track.add_note_block(["D4"], [2], [0.5])
    track.add_note_block(["C4"], [1], [0.5])
    track.add_note_block(["C4"], [1], [0.5])
    track.add_note_block(["G4"], [1], [0.5])
    track.add_note_block(["G4"], [1], [0.5])
    track.add_note_block(["A4"], [1], [0.5])
    track.add_note_block(["A4"], [1], [0.5])
    track.add_note_block(["G4"], [2], [0.5])
    track.add_note_block(["F4"], [1], [0.5])
    track.add_note_block(["F4"], [1], [0.5])
    track.add_note_block(["E4"], [1], [0.5])
    track.add_note_block(["E4"], [1], [0.5])
    track.add_note_block(["D4"], [1], [0.5])
    track.add_note_block(["D4"], [1], [0.5])
    track.add_note_block(["C4"], [2], [0.5])
    track.generate_waveform()
    print(track.calculate_pitch_range())
    sd.play(track.waveform, samplerate=track.sample_rate)
    sd.wait()
if __name__ == "__main__":
    play_little_star()
