import numpy as np
import pytest
from src.timbre.oscillator import oscillator  # 修改为实际路径

def test_waveform_shapes_and_types():
    t = np.linspace(0, 1.0, 1000, endpoint=False)
    frequency = 440
    for wave_type in ['sine', 'square', 'sawtooth', 'triangle']:
        wave = oscillator(wave_type, frequency, t)
        assert isinstance(wave, np.ndarray)
        assert wave.shape == t.shape
        assert np.all(np.isfinite(wave))

def test_waveform_ranges():
    t = np.linspace(0, 1.0, 1000, endpoint=False)
    frequency = 440

    sine_wave = oscillator('sine', frequency, t)
    assert np.all(sine_wave <= 1) and np.all(sine_wave >= -1)

    square_wave = oscillator('square', frequency, t)
    assert set(np.unique(square_wave)).issubset({-1, 0, 1})  # np.sign 可以包含 0

    saw_wave = oscillator('sawtooth', frequency, t)
    assert saw_wave.max() <= 1 and saw_wave.min() >= -1

    tri_wave = oscillator('triangle', frequency, t)
    assert tri_wave.max() <= 1 and tri_wave.min() >= -1

def test_invalid_wave_type():
    t = np.linspace(0, 1.0, 1000, endpoint=False)
    with pytest.raises(ValueError):
        oscillator('invalid_type', 440, t)
