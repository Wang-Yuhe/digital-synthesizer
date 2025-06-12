import numpy as np
from src.timbre.adsr import apply_adsr

def test_adsr_preserves_length():
    sample_rate = 44100
    duration = 1  # 1 second
    waveform = np.ones(int(sample_rate * duration))

    result = apply_adsr(waveform.copy(), sample_rate=sample_rate)

    assert len(result) == len(waveform)

def test_adsr_applies_envelope_effect():
    sample_rate = 1000
    waveform = np.ones(1000)

    result = apply_adsr(
        waveform.copy(),
        sample_rate=sample_rate,
        attack_time=0.1,
        decay_time=0.1,
        sustain_level=0.5,
        release_time=0.2
    )

    # 检查开头是上升趋势（attack阶段）
    assert result[1] > result[0]
    # 检查 sustain 阶段值基本维持在 sustain_level 附近
    sustain_start = int(0.2 * sample_rate)
    sustain_end = int(0.8 * sample_rate)
    sustain_segment = result[sustain_start:sustain_end]
    assert np.allclose(sustain_segment.mean(), 0.5, atol=0.1)
    # 检查结尾趋近于 0（release 阶段）
    assert result[-1] < 0.05

def test_adsr_short_waveform():
    """测试当波形比总 adsr 时间还短时，envelope 是否被裁剪"""
    waveform = np.ones(10)
    result = apply_adsr(waveform.copy(), sample_rate=1000, attack_time=0.01, decay_time=0.01, release_time=0.01)
    assert len(result) == len(waveform)
    assert np.max(result) <= 1
    assert np.min(result) >= 0

def test_adsr_output_type():
    """检查返回类型和不改变原始波形"""
    waveform = np.ones(100)
    original = waveform.copy()
    result = apply_adsr(waveform, sample_rate=1000)
    assert isinstance(result, np.ndarray)
    assert not np.allclose(original, result)
