import numpy as np
import pytest
from src.timbre.panning import panning, dynamic_panning

def test_preprocess_stereo_to_mono():
    stereo_wave = np.stack([np.ones(1000), np.zeros(1000)], axis=1)
    output = dynamic_panning(stereo_wave, start_pan=0.0, end_pan=0.0, chunk_size=256)
    # 应该平均为 0.5
    np.testing.assert_allclose(output[:, 0], 0.25, atol=1e-6)
    np.testing.assert_allclose(output[:, 1], 0.25, atol=1e-6)

def test_preprocess_single_column_to_mono():
    wave = np.ones((1000, 1))
    output = dynamic_panning(wave, start_pan=0.0, end_pan=0.0, chunk_size=256)
    np.testing.assert_allclose(output[:, 0], 0.5)
    np.testing.assert_allclose(output[:, 1], 0.5)

def test_preprocess_flat_input():
    wave = np.ones(1000)
    output = dynamic_panning(wave, start_pan=0.0, end_pan=0.0, chunk_size=256)
    np.testing.assert_allclose(output[:, 0], 0.5)
    np.testing.assert_allclose(output[:, 1], 0.5)

def test_invalid_channel_shape_raises():
    wave = np.ones((1000, 3))  # 3 通道非法
    with pytest.raises(ValueError):
        dynamic_panning(wave, start_pan=0.0, end_pan=0.0, chunk_size=256)

    wave = np.ones((1000, 0))  # 0 通道非法
    with pytest.raises(ValueError):
        dynamic_panning(wave, start_pan=0.0, end_pan=0.0, chunk_size=256)

def test_panning_single_channel_center():
    wave = np.ones(1000)
    stereo = panning(wave, 0.0)
    assert stereo.shape == (1000, 2)
    np.testing.assert_allclose(stereo[:, 0], 0.5)
    np.testing.assert_allclose(stereo[:, 1], 0.5)

def test_panning_left_and_right():
    wave = np.ones(1000)
    left = panning(wave, -1.0)
    right = panning(wave, 1.0)

    np.testing.assert_allclose(left[:, 0], 1.0)
    np.testing.assert_allclose(left[:, 1], 0.0)

    np.testing.assert_allclose(right[:, 0], 0.0)
    np.testing.assert_allclose(right[:, 1], 1.0)

def test_panning_from_stereo_input():
    wave = np.ones((1000, 2))  # stereo input
    stereo = panning(wave, 0.0)
    assert stereo.shape == (1000, 2)
    np.testing.assert_allclose(stereo[:, 0], 0.5)
    np.testing.assert_allclose(stereo[:, 1], 0.5)

def test_invalid_shape_raises():
    wave = np.ones((1000, 3))  # unsupported shape
    with pytest.raises(ValueError):
        panning(wave, 0.0)

def test_dynamic_panning_shape_and_range():
    wave = np.ones(2048)
    stereo = dynamic_panning(wave, start_pan=-1.0, end_pan=1.0, chunk_size=512)
    assert stereo.shape == (2048, 2)

    # 声像从左向右，左声道应该减小，右声道应该增加
    assert stereo[0, 0] > stereo[-1, 0]
    assert stereo[0, 1] < stereo[-1, 1]

def test_dynamic_panning_handles_short_chunks():
    wave = np.ones(10)
    stereo = dynamic_panning(wave, start_pan=-1.0, end_pan=1.0, chunk_size=1)
    assert stereo.shape == (10, 2)
    assert np.all(stereo >= 0.0)
    assert np.all(stereo <= 1.0)
