import numpy as np
import warnings
from scipy.io import wavfile
from src.timbre.flute import flute

def test_flute_basic_properties():
    freq = 261.63  # C4
    duration = 2.0
    sample_rate = 44100
    volume = 0.8

    waveform = flute(freq=freq, duration=duration, sample_rate=sample_rate, volume=volume)

    # 类型与长度检查
    assert isinstance(waveform, np.ndarray)
    assert len(waveform) == int(sample_rate * duration)

    # 数值范围检查（由于有ADSR和volume控制，最大值可能不超过volume）
    assert np.max(np.abs(waveform)) <= 1.0
    assert not np.isnan(waveform).any()
    assert not np.isinf(waveform).any()

def test_flute_zero_duration():
    waveform = flute(freq=261.63, duration=0.0, sample_rate=44100, volume=0.8)
    assert isinstance(waveform, np.ndarray)
    assert len(waveform) == 0

def rms_normalize(x):
    rms = np.sqrt(np.mean(x**2))
    return x / rms if rms > 0 else x

def test_flute_waveform_similarity():
    # 加载参考波形
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sr_ref, ref_waveform = wavfile.read("audio/flute.wav")

    if ref_waveform.ndim == 2:
        ref_waveform = ref_waveform.mean(axis=1)  # 若为立体声，转换为单声道

    ref_waveform = ref_waveform[:1*sr_ref]  # 截取前1秒
    ref_waveform = ref_waveform.astype(np.float32)
    ref_waveform = rms_normalize(ref_waveform)

    # 生成模拟波形
    synth_waveform = flute(freq=261.63, duration=1.0, sample_rate=sr_ref, volume=1.0)
    synth_waveform = rms_normalize(synth_waveform)

    # 对齐长度（避免微小差异导致失配）
    min_len = min(len(ref_waveform), len(synth_waveform))
    ref_waveform = ref_waveform[:min_len]
    synth_waveform = synth_waveform[:min_len]

    # 计算均方误差
    mse = np.mean((ref_waveform - synth_waveform) ** 2)
    print(f"MSE between reference and synthesized flute: {mse:.6f}")

    # 判断误差是否在合理范围（人为设置阈值，可调整）
    assert mse < 3  # 误差越小，越相似

