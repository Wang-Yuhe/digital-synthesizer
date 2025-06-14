"""数字音乐合成器主控类"""
import numpy as np
import sounddevice as sd
from scipy.io import wavfile

from src.track import Track
from src.timbre.panning import dynamic_panning
class DigitalSynthesizer:
    """数字音乐合成器主控类。

    管理多个音轨（Track），可生成混合音频波形，播放或保存为音频文件。
    """

    def __init__(self, bpm: int = 120, sample_rate: int = 44100, volume: float = 1.0):
        """
        初始化合成器参数。

        Args:
            bpm (int): 每分钟节拍数（默认 120）。
            sample_rate (int): 采样率（Hz），默认 44100。
            volume (float): 主音量（0.0 ~ 1.0），默认 1.0。
        """
        self.tracks = []  # List[Track]
        self.waveform = None  # ndarray
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.audio_engine = None
        self.volume = volume

    def add_track_by_property(self, timbre: str, pitch_range: str, bpm: int,
                              sample_rate: int, volume: float) -> Track:
        """
        根据属性创建并添加一条音轨。

        Args:
            timbre (str): 音色类型。
            pitch_range (str): 音高范围。
            bpm (int): 音轨节拍速度。
            sample_rate (int): 音轨采样率。
            volume (float): 音轨音量。

        Returns:
            Track: 新增的音轨实例。
        """
        track_id = len(self.tracks)
        track = Track(timbre, pitch_range, bpm, sample_rate, volume, track_id)
        self.tracks.append(track)
        return track

    def add_track(self, track: Track) -> Track:
        """
        添加已有的音轨对象。

        Args:
            track (Track): 待添加的音轨对象。

        Returns:
            Track: 添加后的音轨。
        """
        track_id = len(self.tracks)
        track.track_id = track_id
        self.tracks.append(track)
        return track

    def remove_track(self, track_id: int) -> bool:
        """
        根据 track_id 删除音轨。

        Args:
            track_id (int): 要删除的音轨索引。

        Returns:
            bool: 删除成功返回 True，否则返回 False。
        """
        if track_id < 0 or track_id >= len(self.tracks):
            return False
        del self.tracks[track_id]
        for i, track in enumerate(self.tracks):
            track.track_id = i
        return True

    def set_bpm(self, bpm: int) -> None:
        """
        设置合成器的节拍速度。

        Args:
            bpm (int): 每分钟节拍数。
        """
        self.bpm = bpm

    def generate_waveform(self) -> np.ndarray:
        """
        根据所有音轨生成合成波形。

        Returns:
            waveform (np.ndarray): 合成的音频数据。
        """
        max_len = 0
        for track in self.tracks:
            track.generate_waveform()
            max_len = max(max_len, len(track.waveform))
        self.waveform = np.zeros(max_len)
        for track in self.tracks:
            if track.waveform is not None:
                self.waveform[:len(track.waveform)] += track.waveform
        self.waveform *= self.volume
        return self.waveform


    def play_for_preview(self) -> None:
        """播放音频"""
        sd.play(self.waveform, samplerate=self.sample_rate)
        sd.wait()

    def save_to_file(self, filename: str) -> bool:
        """
        将当前音频波形保存为 WAV 文件。

        Args:
            filename (str): 文件名（不带扩展名）。

        Returns:
            bool: 保存成功返回 True。
        """
        wavfile.write(filename+'.wav', self.sample_rate, self.waveform.astype(np.float32))

    def open_file(self, filename: str) -> bool:
        """打开文件"""

def play_instance(): # pragma: no cover
    """播放实例"""
    synthesizer = DigitalSynthesizer(volume=0.5)

    # 伴奏与旋律均用Track类，节拍、音量明确，block_id从0开始

    # 旋律音轨
    melody = Track(timbre="piano")
    melody.add_note_block("C4,C4,D4,C4,F4,E4".split(","), [0.5, 0.5, 1, 1, 1, 2], start_beat=[0, 0.5, 1, 2, 3, 4])
    melody.add_note_block("C4,C4,D4,C4,G4,F4".split(","), [0.5, 0.5, 1, 1, 1, 2], start_beat=[0, 0.5, 1, 2, 3, 4])
    melody.add_note_block("C4,C4,C5,A4,F4,E4,D4".split(","), [0.5, 0.5, 1, 1, 1, 1, 1], start_beat=[0, 0.5, 1, 2, 3, 4, 5])
    melody.add_note_block("Bb4,Bb4,A4,F4,G4,F4".split(","), [0.5, 0.5, 1, 1, 1, 2], start_beat=[0, 0.5, 1, 2, 3, 4])

    accompaniment = Track(timbre="piano")
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

    synthesizer.add_track(melody1)
    synthesizer.add_track(accompaniment1)
    synthesizer.generate_waveform()
    synthesizer.waveform = dynamic_panning(synthesizer.waveform)
    synthesizer.play_for_preview()

if __name__ == "__main__": # pragma: no cover
    play_instance()
