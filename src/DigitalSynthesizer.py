from Track import Track
from AudioEngine import AudioEngine
import numpy as np
import sounddevice as sd
class DigitalSynthesizer:
    """数字音乐合成器主控类"""
    
    def __init__(self):
        self.tracks = []  # List[Track]
        self.waveform = None  # ndarray
        self.bpm = 60
        self.sample_rate = 44100
        self.audio_engine = None
        self.volume = 1

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
    synthesizer = DigitalSynthesizer()

    # 伴奏与旋律均用Track类，节拍、音量明确，block_id从0开始

    # 旋律音轨
    melody = Track("piano", "A4-C6", 120, 44100, 0.7, 0)
    melody.add_note_block(["C4"], [1], [], 0)


    synthesizer.add_track(melody)
    synthesizer.add_track(accompaniment)
    synthesizer.generate_waveform()
    synthesizer.play_for_preview()

if __name__ == "__main__":
    play_instance()