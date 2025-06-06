"""滤波器"""
from scipy.signal import butter, lfilter

def lowpass_filter(waveform, wc, N=4, sample_rate=44100):#wc截止频率,butter平稳的滤波器
    """低通滤波器"""
    b,a = butter(N, wc, fs=sample_rate)
    #scipy 的滤波器设计函数要求频率是相对于 奈奎斯特频率（Nyquist = sample_rate / 2）的比例
    #用fs参数不需要手动除了
    return lfilter(b, a, waveform)

def band_filter(waveform, wc, N=4, sample_rate=44100):
    """带通滤波器"""
    b, a = butter(N, wc, btype='band', fs=sample_rate)
    return lfilter(b, a, waveform)
