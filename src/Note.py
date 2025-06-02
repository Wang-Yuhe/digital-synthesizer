import numpy as np
import scipy.io.wavfile as wavfile
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.signal as sg


def rms_normalize(waveform):
    """使用RMS归一化波形"""
    rms = np.sqrt(np.mean(waveform ** 2))
    if rms > 0:
        return waveform / rms
    return waveform


class Note:
    """音符类"""

    def __init__(self, timbre: str, bpm: int, sample_rate: int, note_name, beat_time, volume, note_id):
        # 修改初始化方式，note_name输入格式为:音名(C,C#...B)+数字(0~8)
        # in接口
        self.note_id = note_id
        self.note_name = note_name
        self.beat_time = beat_time  # 节拍数
        self.volume = volume  # 音量范围 0-1
        self.timbre = timbre

        self.duration = beat_time / bpm * 60
        self.sample_rate = sample_rate

        # out接口
        self.waveform = None  # ndarray

    def note2freq(self, note):  # 音符转频率,note格式为C4
        # C,C#,D,D#,E,F,F#,G,G#,A,A#,B
        note_map = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
                    'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        for k in sorted(note_map.keys(), key=lambda x: -len(x)):
            if note.startswith(k):
                octave = int(note[len(k):])
                midi_num = 12 * (octave + 1) + note_map[k]
                return 440.0 * (2 ** ((midi_num - 69) / 12))

        raise ValueError("Invalid note format")

    def generate_waveform(self) -> np.ndarray:
        freq = self.note2freq(self.note_name)
        if self.timbre == "piano":
            t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)

            # 增加谐波成分(决定音色)，基波+若干谐波(振幅递减，频率整数倍)
            harmonics = [1, 0.340, 0.102, 0.085, 0.070, 0.065, 0.028, 0.010, 0.014, 0.012, 0.013, 0.004]
            self.waveform = sum(self.volume * amplitude * np.sin(2 * np.pi * freq * (i + 1) * t)
                                for i, amplitude in enumerate(harmonics))
            self.waveform /= np.max(np.abs(self.waveform))

            # 增加adsr包络，使振幅更自然
            self.apply_adsr(self.duration * 0.01, self.duration * 0.03, 0.4, self.duration * 0.8)
            # self.waveform=self.waveform*(t**0.01*np.exp(-3*t))

            # wavfile.write('generated_audio.wav', self.sample_rate, self.waveform.astype(np.float32))
            sd.play(self.waveform, samplerate=self.sample_rate)  # 在线播放
            sd.wait()
        if self.timbre == "violin":
            t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)

            # 小提琴的谐波成分更丰富，高频部分衰减较慢
            harmonics = [0.5, 0.8, 0.3, 0.15, 0.1, 0.08, 0.05, 0.03, 0.02, 0.01]  # 基频相对较弱，谐波更丰富
            self.waveform = sum(self.volume * amplitude * np.sin(2 * np.pi * freq * (i + 1) * t)
                                for i, amplitude in enumerate(harmonics))
            vibrato_depth = 0.02  # 颤音深度
            vibrato_rate = 6  # 颤音频率(Hz)
            vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
            self.waveform *= vibrato
            self.waveform /= np.max(np.abs(self.waveform))

            # 小提琴的ADSR包络 - 更慢的起音和释音
            attack_time = self.duration * 0.1  # 更长的起音时间
            decay_time = self.duration * 0.2  # 更长的衰减时间
            sustain_level = 0.7  # 较高的持续电平
            release_time = self.duration * 0.3  # 更长的释音时间

            self.apply_adsr(attack_time, decay_time, sustain_level, release_time)
            sd.play(self.waveform, samplerate=self.sample_rate)
            sd.wait()
        if self.timbre == "viola":
            t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)

            # 增加谐波复杂性，以增强粗糙感
            harmonics = [1.0, 0.5, 0.3, 0.2, 0.1]  # 增加一些高频成分以增加粗糙感
            self.waveform = sum(self.volume * amplitude * np.sin(2 * np.pi * freq * (i + 1) * t)
                                for i, amplitude in enumerate(harmonics))

            # 添加低频噪声以增强低频特性
            noise_amplitude = 0.2  # 增加噪声幅度
            noise = np.random.normal(0, noise_amplitude, len(t))

            # 低通滤波器：使用简单的移动平均来增强低频噪声
            window_size = 100  # 调整窗口大小以平衡低频和粗糙感
            low_pass_noise = np.convolve(noise, np.ones(window_size) / window_size, mode='same')

            self.waveform += low_pass_noise

            # 增加颤音效果以增加不稳定性
            vibrato_depth = 0.05
            vibrato_rate = 10
            vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
            self.waveform *= vibrato

            # 归一化
            self.waveform /= np.max(np.abs(self.waveform))

            # 增加非线性失真以增加粗糙感
            self.waveform = np.tanh(2.5 * self.waveform)  # 增加失真系数以增强粗糙感

            # 应用ADSR包络，增强低频持续感
            attack_time = self.duration * 0.05
            decay_time = self.duration * 0.1
            sustain_level = 0.6
            release_time = self.duration * 0.85
            self.apply_adsr(attack_time, decay_time, sustain_level, release_time)

            sd.play(self.waveform, samplerate=self.sample_rate)
            sd.wait()
        if self.timbre == "cello":
            t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)

            # 调整谐波成分
            harmonics = [1.0, 0.5, 0.3, 0.2]  # 增加高频成分以增加粗糙感
            self.waveform = sum(self.volume * amplitude * np.sin(2 * np.pi * freq * (i + 1) * t)
                                for i, amplitude in enumerate(harmonics))

            # 增加低频噪声以增强低频特性
            noise_amplitude = 0.25  # 适度增加噪声幅度
            noise = np.random.normal(0, noise_amplitude, len(t))

            # 低通滤波器：使用简单的移动平均来增强低频噪声
            window_size = 120  # 调整窗口大小以平衡低频和粗糙感
            low_pass_noise = np.convolve(noise, np.ones(window_size) / window_size, mode='same')

            self.waveform += low_pass_noise

            # 增加颤音效果以增加不稳定性
            vibrato_depth = 0.04
            vibrato_rate = 10
            vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
            self.waveform *= vibrato

            # 归一化
            self.waveform /= np.max(np.abs(self.waveform))

            # 增加非线性失真以增加粗糙感
            self.waveform = np.tanh(2.0 * self.waveform)

            # 应用ADSR包络
            attack_time = self.duration * 0.05
            decay_time = self.duration * 0.1
            sustain_level = 0.6
            release_time = self.duration * 0.85
            self.apply_adsr(attack_time, decay_time, sustain_level, release_time)

            sd.play(self.waveform, samplerate=self.sample_rate)
            sd.wait()
        if self.timbre == "double_bass":
            t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)

            # 调整谐波成分，以接近低音提琴的音色
            harmonics = [1.0, 0.3, 0.1]  # 减少高频成分，强调低频
            self.waveform = sum(self.volume * amplitude * np.sin(2 * np.pi * freq * (i + 1) * t)
                                for i, amplitude in enumerate(harmonics))

            # 增加低频噪声以增强低频特性
            noise_amplitude = 0.3  # 增加噪声幅度以增强低频特性
            noise = np.random.normal(0, noise_amplitude, len(t))

            # 低通滤波器：使用简单的移动平均来增强低频噪声
            window_size = 150  # 增加窗口大小以增强低频特性
            low_pass_noise = np.convolve(noise, np.ones(window_size) / window_size, mode='same')

            self.waveform += low_pass_noise

            # 增加颤音效果以增加不稳定性
            vibrato_depth = 0.03
            vibrato_rate = 8
            vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
            self.waveform *= vibrato

            # 归一化
            self.waveform /= np.max(np.abs(self.waveform))

            # 增加非线性失真以增加粗糙感
            self.waveform = np.tanh(1.5 * self.waveform)  # 适度增加失真系数

            # 应用ADSR包络，模仿低音提琴的发音特性
            attack_time = self.duration * 0.1
            decay_time = self.duration * 0.2
            sustain_level = 0.5
            release_time = self.duration * 0.7
            self.apply_adsr(attack_time, decay_time, sustain_level, release_time)

            sd.play(self.waveform, samplerate=self.sample_rate)
            sd.wait()
        return rms_normalize(self.waveform)

    def show_time_and_freq_domain(self):
        t = np.linspace(0, self.duration, len(self.waveform), endpoint=False)

        # -------- 时域图 --------
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(t, self.waveform)
        plt.title(f"Time Domain: {self.note_name} ({self.timbre})")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)

        # -------- 频域图 --------
        N = len(self.waveform)
        freq_domain = np.fft.fft(self.waveform)
        freq = np.fft.fftfreq(N, d=1 / self.sample_rate)

        # 取正频率部分
        half_N = N // 2
        magnitude = np.abs(freq_domain[:half_N])
        magnitude /= np.max(magnitude)  # 归一化
        freq = freq[:half_N]

        plt.subplot(1, 2, 2)
        plt.plot(freq, magnitude)  # 转换成分贝
        plt.title("Frequency Domain")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Normalized Amplitude")
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    def apply_adsr(self, attack_time=0.01, decay_time=0.1, sustain_level=0.8, release_time=0.2):
        """增加adsr包络曲线"""
        total_samples = len(self.waveform)

        attack_samples = int(self.sample_rate * attack_time)
        decay_samples = int(self.sample_rate * decay_time)
        release_samples = int(self.sample_rate * release_time)
        sustain_samples = total_samples - (attack_samples + decay_samples + release_samples)
        sustain_samples = max(sustain_samples, 0)

        # 各阶段的包络
        attack_env = np.linspace(0, 1, attack_samples)
        decay_env = np.linspace(1, sustain_level, decay_samples)
        sustain_env = np.full(sustain_samples, sustain_level)  # 保持不变
        release_env = np.linspace(sustain_level, 0, release_samples)

        envelope = np.concatenate([attack_env, decay_env, sustain_env, release_env])

        # 截断或填补以匹配 wave 长度
        if len(envelope) > total_samples:
            envelope = envelope[:total_samples]
        else:
            envelope = np.pad(envelope, (0, total_samples - len(envelope)))

        self.waveform *= envelope

    def generate_audio_data(self) -> np.ndarray:
        """生成音频数据"""
        pass


if __name__ == "__main__":
    note = Note("piano", 60, 44100, "E4", 2, 0.5, 0)
    note.generate_waveform()
    note = Note("violin", 60, 44100, "E4", 2, 0.5, 0)
    note.generate_waveform()
    note = Note("viola", 60, 44100, "E4", 2, 0.5, 0)
    note.generate_waveform()
    note = Note("cello", 60, 44100, "E4", 2, 0.5, 0)
    note.generate_waveform()
    note = Note("double_bass", 60, 44100, "E4", 2, 0.5, 0)
    note.generate_waveform()