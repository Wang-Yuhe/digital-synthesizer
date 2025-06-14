"""滤波器"""
from scipy.signal import butter, lfilter

def lowpass_filter(waveform, wc, N=4, sample_rate=44100):#wc截止频率,butter平稳的滤波器
    """
    对输入波形应用低通滤波器（Low-pass Filter），滤除高于截止频率 wc 的频率成分。

    Args:
        waveform (np.ndarray): 输入的音频信号（一维波形数组）
        wc (float): 截止频率（单位: Hz），滤除高于此频率的频率成分
        N (int): 滤波器的阶数，阶数越高，滤波器越陡峭（默认 4）
        sample_rate (int): 音频采样率（默认 44100Hz）

    Returns:
        np.ndarray: 滤波后的音频波形
    """
    b,a = butter(N, wc, fs=sample_rate)
    #scipy 的滤波器设计函数要求频率是相对于 奈奎斯特频率（Nyquist = sample_rate / 2）的比例
    #用fs参数不需要手动除了
    return lfilter(b, a, waveform)

def band_filter(waveform, wc, N=4, sample_rate=44100):
    """
    对输入波形应用带通滤波器（Band-pass Filter），保留指定频带范围内的频率分量。

    Args:
        waveform (np.ndarray): 输入的音频信号（一维波形数组）
        wc (tuple[float, float]): 截止频率范围（低频, 高频），例如 (300, 3000)
        N (int): 滤波器的阶数（默认 4）
        sample_rate (int): 音频采样率（默认 44100Hz）

    Returns:
        np.ndarray: 滤波后的音频波形
    """
    b, a = butter(N, wc, btype='band', fs=sample_rate)
    return lfilter(b, a, waveform)
