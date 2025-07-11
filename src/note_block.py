"""音块类"""
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

from src.note import Note
class NoteBlock:
    """音块类。

    用于组织多个音符（Note），具备生成波形、绘图、添加/删除音符的功能。
    每个音块中音符共享相同的音色、BPM 和采样率。
    """

    def __init__(self, timbre: str = "piano", bpm: int = 120, sample_rate: int = 44100,
                 note_names: list[str] = None, beat_times: list[float] = None,
                 start_beat: list[float] = None, volume: list[float] = None, block_id: int = 0):
        """
        初始化音块。

        Args:
            timbre (str): 音色名称，例如 "piano"。
            bpm (int): 每分钟节拍数（Beats Per Minute）。
            sample_rate (int): 采样率（Hz）。
            note_names (list[str], optional): 音符名称列表（如 ["C4", "E4"]）。
            beat_times (list[float], optional): 每个音符持续的节拍数。
            start_beat (list[float], optional): 每个音符起始节拍位置。
            volume (list[float], optional): 每个音符的音量（0.0 ~ 1.0）。
            block_id (int): 音块编号。
        """
        # 设置默认值（避免共享默认列表）
        if note_names is None:
            note_names = ["C4", "E4", "G4"]
        if beat_times is None:
            beat_times = [1, 1, 1]
        if start_beat is None:
            start_beat = [0, 0, 0]
        if volume is None:
            volume = [1, 1, 1]

        # in接口
        self.block_id = block_id
        self.timbre = timbre
        self.bpm = bpm
        self.sample_rate = sample_rate

        # 应用方法时需要修改的属性：
        self.note_names = []
        self.beat_times = []
        self.start_beat = []
        self.volume = []
        self.notes = []  # List[Note]

        for i, note_name in enumerate(note_names):
            self.add_note(note_name, beat_times[i], volume[i], start_beat[i])
        for i, note in enumerate(self.notes):
            note.note_id = i

        # out接口
        self.waveform = None  # ndarray


    def generate_waveform(self) -> np.ndarray:
        """
        生成音块对应的音频波形。

        Returns:
            waveform (np.ndarray): 该音块的音频波形数据。
        """
        if len(self.notes) == 0:
            self.waveform = np.zeros(0)
            return self.waveform
        max_len = 0
        # 填充不从0开始的音符
        for note in self.notes:
            if self.start_beat[note.note_id] > 0:
                note.generate_waveform()
                # 在音符开始前添加休止符
                silence = np.zeros(int(self.start_beat[note.note_id] / self.bpm * 60 * self.sample_rate))
                note.waveform = np.concatenate((silence, note.waveform))
                max_len = max(max_len, len(note.waveform))
            else:
                note.generate_waveform()
                max_len = max(max_len, len(note.waveform))
        # 填充音符长度不一致的音符
        for note in self.notes:
            if len(note.waveform) < max_len:
                silence = np.zeros(max_len - len(note.waveform))
                note.waveform = np.concatenate((note.waveform, silence))
        notes_waveform = [note.waveform for note in self.notes]
        self.waveform = sum(notes_waveform) if len(notes_waveform) > 1 else notes_waveform[0]
        return self.waveform

    def show_time_domain(self):
        """
        绘制音块波形的时域图。
        """
        if len(self.waveform) == 0:
            print("No waveform data to display.")
            return
        t = np.linspace(0, (self.start_beat[0]+max(self.beat_times)-1)/self.bpm*60, len(self.waveform), endpoint=False)
        # -------- 时域图 --------
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(t, self.waveform)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()

    # 由于同一音块的音色、bpm和采样率相同，所以不需要传参
    def add_note(self, note_name: str, beat_time: float, volume: float, start_beat: float = 0) -> bool:
        """
        添加一个音符到音块中。

        Args:
            note_name (str): 音符名称（如 "C4"）。
            beat_time (float): 音符持续的节拍数。
            volume (float): 音符音量（0.0 ~ 1.0）。
            start_beat (float): 音符开始的节拍位置。

        Returns:
            bool: 添加成功返回 True。
        """
        note = Note(self.timbre, self.bpm, self.sample_rate, note_name, beat_time, volume, len(self.notes))
        self.note_names.append(note_name)
        self.beat_times.append(beat_time)
        self.volume.append(volume)
        self.start_beat.append(start_beat)
        self.notes.append(note)
        return True

    def remove_note(self, note_id: int) -> bool:
        """
        根据索引删除一个音符。

        Args:
            note_id (int): 要删除的音符编号。

        Returns:
            bool: 删除成功返回 True，失败返回 False。
        """
        if note_id < 0 or note_id >= len(self.notes):
            return False
        del self.notes[note_id]
        del self.note_names[note_id]
        del self.beat_times[note_id]
        del self.volume[note_id]
        del self.start_beat[note_id]
        for i, note in enumerate(self.notes):
            note.note_id = i
        return True

if __name__ == "__main__": # pragma: no cover
    # 测试代码
    note_block = NoteBlock(timbre="piano",note_names=["C4", "E4", "G4"],
                           beat_times=[3, 2, 1], volume=[0.5, 0.5, 0.5],
                           start_beat=[0, 1, 2], block_id=0)
    note_block.remove_note(2)
    note_block.add_note("G4", 1, 0.5, 2)
    print(note_block.note_names)
    print(note_block.beat_times)
    print(note_block.start_beat)

    note_block.generate_waveform()
    #note_block.show_time_domain()

    # for note in note_block.notes:
    #     plt.plot(range(len(note.waveform)), note.waveform)
    plt.subplot(3, 1, 1)
    plt.plot(range(len(note_block.notes[0].waveform)), note_block.notes[0].waveform, label="C4")
    plt.subplot(3, 1, 2)
    plt.plot(range(len(note_block.notes[1].waveform)), note_block.notes[1].waveform, label="E4")
    plt.subplot(3, 1, 3)
    plt.plot(range(len(note_block.notes[2].waveform)), note_block.notes[2].waveform, label="G4")
    plt.legend()
    plt.title("Waveform")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

    sd.play(note_block.waveform, samplerate=note_block.sample_rate)
    sd.wait()
