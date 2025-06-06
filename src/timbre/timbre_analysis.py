"""基于单音的音色分析"""
import numpy as np
import librosa
import matplotlib.pyplot as plt

def timbre_analysis(filename: str) -> list[float]:
    """分析谐波系数"""
    # 读取 WAV 文件
    waveform, sample_rate = librosa.load(filename, sr=None)
    # 使用前两秒的音频进行傅立叶分析，所以请确保前两秒是乐器的声音
    waveform = waveform[: sample_rate * 2 + 1]

    # 傅里叶变换
    spectrum = np.fft.rfft(waveform)
    freqs = np.fft.rfftfreq(len(waveform), d=1/sample_rate)
    magnitude = np.abs(spectrum)

    # 检测基频
    f0 = librosa.yin(waveform, fmin=50, fmax=2000, sr=sample_rate)[0]

    # 提取前10个谐波的幅值
    harmonics = []
    for n in range(1, 17):
        harmonic_freq = f0 * n
        idx = np.argmin(np.abs(freqs - harmonic_freq))
        harmonics.append(magnitude[idx])

    # 归一化
    harmonics = np.array(harmonics)
    harmonics /= harmonics[0]  # 基频幅值归一为 1.0

    return harmonics.tolist()


# if __name__ == "__main__":
#     filename = "audio/flute.wav"
#     harmonics = timbre_analysis(filename)
#     harmonics = [round(h, 3) for h in harmonics]
#     print("Harmonics:", harmonics)

def adsr_analysis(filename: str) -> dict:
    """分析adsr包络参数"""
    waveform, sample_rate = librosa.load(filename, sr=None)
    waveform = librosa.util.normalize(waveform)

    # 计算音量包络（RMS）
    frame_length = 2048
    hop_length = 512
    rms = librosa.feature.rms(y=waveform, frame_length=frame_length, hop_length=hop_length)[0]
    times = librosa.times_like(rms, sr=sample_rate, hop_length=hop_length)
    envelope = rms / np.max(rms)

    # 找 Attack 峰
    peak_idx = np.argmax(envelope)
    peak_time = times[peak_idx]
    attack_time = peak_time

    # 找 Decay 到 Sustain（设定阈值）
    sustain_level = 0.3  # 设定一个阈值，表示sustain的音量比例
    decay_idx = peak_idx
    while decay_idx < len(envelope) and envelope[decay_idx] > sustain_level:
        decay_idx += 1

    decay_time = times[decay_idx] - peak_time

    # Sustain：从 decay 后保持到包络明显下降为止
    release_start_idx = decay_idx
    threshold = 0.1
    while release_start_idx < len(envelope) and envelope[release_start_idx] > threshold:
        release_start_idx += 1

    sustain_time = times[release_start_idx] - times[decay_idx]

    # Release：从 sustain 结束到归零
    release_time = times[-1] - times[release_start_idx]

    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(waveform, sr=sample_rate)
    plt.title("Waveform (Time Domain)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()

    times=attack_time+decay_time+sustain_time+release_time

    return {
        "attack_rate": attack_time/times,
        "decay_rate": decay_time/times,
        "sustain_level": sustain_level,
        "sustain_rate": sustain_time/times,
        "release_rate": release_time/times
    }

if __name__ == "__main__":
    filename1 = "audio/flute.wav"
    #filename = "E:/digital-synthesizer/audio/harp.mp3"
    harmonics1 = timbre_analysis(filename1)
    harmonics1 = [round(h, 3) for h in harmonics1]
    print("Harmonics:", harmonics1)

    adsr = adsr_analysis(filename1)
    print("Adsr:", adsr)
