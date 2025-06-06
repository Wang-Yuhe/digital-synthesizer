"""音频引擎类"""
import numpy as np
class AudioEngine:
    """
    音频引擎

    暂时没有确定该类如何作用，是否保留
    """

    def __init__(self):
        self.sample_rate = 44100

    def play_audio(self, data: np.ndarray) -> None:
        """播放音频"""

    def stop_playback(self) -> None:
        """停止播放"""
