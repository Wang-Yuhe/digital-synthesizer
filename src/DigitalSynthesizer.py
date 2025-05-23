from Track import Track
from AudioEngine import AudioEngine
import numpy as np
import sounddevice as sd
class DigitalSynthesizer:
    """数字音乐合成器主控类"""
    
    def __init__(self, bpm: int = 120, sample_rate: int = 44100, volume: float = 1.0):
        self.tracks = []  # List[Track]
        self.waveform = None  # ndarray
        self.bpm = 60
        self.sample_rate = 44100
        self.audio_engine = None
        self.volume = volume

    def add_track(self, timbre: str, pitch_range: str, bpm: int, sample_rate: int, volume: float) -> Track:
        """添加音轨"""
        track_id = len(self.tracks)
        track = Track(timbre, pitch_range, bpm, sample_rate, volume, track_id)
        self.tracks.append(track)
        return track
    
    def add_track(self, track: Track) -> Track:
        """添加音轨"""
        track_id = len(self.tracks)
        track.track_id = track_id
        self.tracks.append(track)
        return track
        
    def remove_track(self, track_id: int) -> bool:
        """删除音轨"""
        if track_id < 0 or track_id >= len(self.tracks):
            return False
        del self.tracks[track_id]
        for i in range(len(self.tracks)):
            self.tracks[i].track_id = i
        return True

    def set_bpm(self, bpm: int) -> None:
        """设置乐曲bpm"""
        self.bpm = bpm
        
    def generate_waveform(self) -> np.ndarray:
        """生成音频数据"""
        max_len = 0
        for track in self.tracks:
            track.generate_waveform()
            max_len = max(max_len, len(track.waveform))
        self.waveform = np.zeros(max_len)
        for track in self.tracks:
            if track.waveform is not None:
                self.waveform[:len(track.waveform)] += track.waveform * track.volume
        return self.waveform


    def play_for_preview(self) -> None:
        """播放音频"""
        sd.play(self.waveform, samplerate=self.sample_rate)
        sd.wait()
        
    def save_to_file(self, filename: str) -> bool:
        """保存为文件"""
        pass
        
    def open_file(self, filename: str) -> bool:
        """打开文件"""
        pass

def play_instance():
    """播放实例"""
    synthesizer = DigitalSynthesizer(volume=0.5)

    # 伴奏与旋律均用Track类，节拍、音量明确，block_id从0开始

    # 旋律音轨
    melody = Track()
    melody.add_note_block("C4,C4,D4,C4,F4,E4".split(","), [0.5, 0.5, 1, 1, 1, 2], start_beat=[0, 0.5, 1, 2, 3, 4])
    melody.add_note_block("C4,C4,D4,C4,G4,F4".split(","), [0.5, 0.5, 1, 1, 1, 2], start_beat=[0, 0.5, 1, 2, 3, 4])
    melody.add_note_block("C4,C4,C5,A4,F4,E4,D4".split(","), [0.5, 0.5, 1, 1, 1, 1, 1], start_beat=[0, 0.5, 1, 2, 3, 4, 5])
    melody.add_note_block("Bb4,Bb4,A4,F4,G4,F4".split(","), [0.5, 0.5, 1, 1, 1, 2], start_beat=[0, 0.5, 1, 2, 3, 4])

    accompaniment = Track()
    accompaniment.add_note_block("F2,C3,G2,E3".split(","),[2,2,2,2],start_beat=[1,1,4,4])
    accompaniment.add_note_block("E2,C3,F2,C3".split(","),[2,2,2,2],start_beat=[1,1,4,4])
    accompaniment.add_note_block("F2,C3,G2,D3".split(","),[2,2,2,2],start_beat=[1,1,4,4])
    accompaniment.add_note_block("F2,A2,G2,C3,F2,C3".split(","),[2,2,1,1,1,1],start_beat=[1,1,3,3,4,4])
    
    melody1 = Track()
    melody1.add_note_block(["E4","F#4","G#4","G#4","F#4","E4","E4"],[1,0.5,0.5,0.5,0.5,0.5,0.5],start_beat=[0,1,1.5,2,2.5,3,3.5])
    accompaniment1 = Track()
    accompaniment1.add_note_block("A1,A2,E3,A3,A1,A2,E3,A3".split(","),[2,2,1,1,1,1,1,1],start_beat=[0,0,1,1,2,2,3,3])

    melody1.add_note_block(["F#4","G#4","F#4","E4","E4","E4"],[1,1,0.5,0.5,0.5,0.5],start_beat=[0,1,2,2.5,3,3.5])
    accompaniment1.add_note_block(["G#1","G#2","E3","G#3","G#1","G#2","E3","G#3"],[2,2,1,1,1,1,1,1],start_beat=[0,0,1,1,2,2,3,3])

    melody1.add_note_block(["F#4","G#4","F#4","G#4"],[1,1,1,1],start_beat=[0,1,2,3])
    accompaniment1.add_note_block(["C#1","C#2","E3","G#3","C#1","C#2","E3","G#3"],[2,2,1,1,1,1,1,1],start_beat=[0,0,1,1,2,2,3,3])

    melody1.add_note_block(["E4","B4","E4","A4","G#4","F#4"],[0.5,0.5,0.5,0.5,0.5,1],start_beat=[0,0.5,1.5,2,2.5,3])
    accompaniment1.add_note_block(["B1","B2","B3","G#3","B1","B2","B3","G#3"],[2,2,1,1,1,1,1,1],start_beat=[0,0,1,1,2,2,3,3])

    synthesizer.add_track(melody)
    synthesizer.add_track(accompaniment)
    synthesizer.generate_waveform()
    synthesizer.play_for_preview()

if __name__ == "__main__":
    play_instance()