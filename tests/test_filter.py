import numpy as np
import pytest
from src.timbre.filter import lowpass_filter, band_filter

def generate_test_waveform(freqs, sample_rate=1000, duration=1.0):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = sum(np.sin(2 * np.pi * f * t) for f in freqs)
    return signal, sample_rate

def test_lowpass_filter_basic():
    waveform, sr = generate_test_waveform([50, 300], sample_rate=1000)
    filtered = lowpass_filter(waveform, wc=100, sample_rate=sr)

    assert isinstance(filtered, np.ndarray)
    assert filtered.shape == waveform.shape
    assert np.var(filtered) < np.var(waveform)  # 滤波应减少能量

def test_band_filter_basic():
    waveform, sr = generate_test_waveform([50, 300], sample_rate=1000)
    filtered = band_filter(waveform, wc=[40, 100], sample_rate=sr)

    assert isinstance(filtered, np.ndarray)
    assert filtered.shape == waveform.shape
    assert np.var(filtered) < np.var(waveform)

def test_lowpass_filter_invalid_wc():
    waveform = np.random.randn(1000)
    with pytest.raises(ValueError):
        lowpass_filter(waveform, wc=-100)  # 非法频率

def test_band_filter_invalid_wc():
    waveform = np.random.randn(1000)
    with pytest.raises(ValueError):
        band_filter(waveform, wc=[100], sample_rate=1000)  # 长度错误

    with pytest.raises(ValueError):
        band_filter(waveform, wc=[-10, 5000], sample_rate=1000)  # 越界
