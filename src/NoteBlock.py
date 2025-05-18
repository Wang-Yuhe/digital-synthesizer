import numpy as np
from Note import Note
import sounddevice as sd
class NoteBlock:
    """音块类"""

    def __init__(self, timbre: str, bpm: int, sample_rate: int, note_names: list[str], 
                 beat_times: list[float], volume: list[float], block_id: int):
        # in接口
        self.block_id = block_id
        self.timbre = timbre
        self.bpm = bpm
        self.sample_rate = sample_rate
        
        # 应用方法时需要修改的属性：
        self.note_names = []
        self.beat_times = []
        self.volume = []
        self.notes = []  # List[Note]
        self.note_count = 0
        for i in range(len(note_names)):
            self.add_note(note_names[i], beat_times[i], volume[i])
        
        # out接口
        self.waveform = None  # ndarray
        
    def generate_waveform(self) -> np.ndarray:
        """产生波形"""
        notes_waveform = [note.generate_waveform() for note in self.notes]
        self.waveform = sum(notes_waveform) if len(notes_waveform) > 1 else notes_waveform[0]
        return self.waveform
    
    # 由于同一音块的音色、bpm和采样率相同，所以不需要传参
    def add_note(self, note_name: str, beat_time: float, volume: float) -> bool:
        """添加音符"""
        id = self.note_count
        note = Note(self.timbre, self.bpm, self.sample_rate, note_name, beat_time, volume, id)
        self.note_count += 1
        self.note_names.append(note_name)
        self.beat_times.append(beat_time)
        self.volume.append(volume)
        self.notes.append(note)
        return True

    def remove_note(self, note_id: int) -> bool:
        """删除音符"""
        if note_id < 0 or note_id >= self.note_count:
            return False
        del self.notes[note_id]
        del self.note_names[note_id]
        del self.beat_times[note_id]
        del self.volume[note_id]
        self.note_count -= 1
        for i in range(self.note_count):
            self.notes[i].note_id = i
        return True

if __name__ == "__main__":
    # 测试代码
    note_block = NoteBlock("piano", 120, 44100, ["C4", "E4", "G4"], [1, 1, 1], [0.5, 0.5, 0.5], 0)
    note_block.remove_note(2)
    note_block.add_note("G4", 1, 0.5)
    note_block.generate_waveform()
    sd.play(note_block.waveform, samplerate=note_block.sample_rate)
    sd.wait()