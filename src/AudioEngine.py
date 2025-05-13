import numpy as np
class AudioEngine:
    """音频引擎"""
    
    def __init__(self):
        self.sample_rate = 44100
        
    def play_audio(self, data: np.ndarray) -> None:
        """播放音频"""
        pass
        
    def stop_playback(self) -> None:
        """停止播放"""
        pass