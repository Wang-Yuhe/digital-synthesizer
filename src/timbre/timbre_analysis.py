import numpy as np
import librosa

def timbre_analysis(filename: str) -> list[float]:
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

if __name__ == "__main__":
    filename = "audio/flute.wav"
    harmonics = timbre_analysis(filename)
    harmonics = [round(h, 3) for h in harmonics]
    print("Harmonics:", harmonics)