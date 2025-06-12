"""Note类测试"""
import pytest
import numpy as np
import io
import sys
from src.note import Note

def test_note_initialization():
    note = Note(timbre="piano", bpm=120, sample_rate=44100, note_name="C4", beat_time=1.0, volume=0.8, note_id=1)
    assert note.note_name == "C4"
    assert note.timbre == "piano"
    assert note.duration == pytest.approx(0.5)
    assert note.volume == 0.8

def test_note_midi_conversion():
    assert Note(note_name="C4").note_midi() == 60
    assert Note(note_name="A4").note_midi() == 69
    assert Note(note_name="C#4").note_midi() == 61
    assert Note(note_name="Bb3").note_midi() == 58

def test_note_comparisons():
    assert Note(note_name="C4") < Note(note_name="D4")
    assert Note(note_name="C4") == Note(note_name="C4")
    assert Note(note_name="E4") > Note(note_name="D#4")

def test_note2freq():
    note = Note(note_name="A4")
    assert note.note2freq("A4") == pytest.approx(440.0, abs=0.01)
    assert note.note2freq("C4") == pytest.approx(261.63, rel=0.01)

def test_generate_waveform():
    note = Note(note_name="C4", timbre="piano", beat_time=1.0)
    waveform = note.generate_waveform()
    assert isinstance(waveform, np.ndarray)
    assert waveform.shape[0] == int(note.sample_rate * note.duration)
    assert np.max(np.abs(waveform)) <= 1.0

def test_rest_waveform():
    note = Note(note_name="rest")
    waveform = note.generate_waveform()
    assert np.allclose(waveform, 0)

def test_invalid_note_format():
    with pytest.raises(ValueError):
        _ = Note(note_name="H#4").note_midi()

def test_unknown_timbre_raises_error():
    note = Note(note_name="C4", timbre="alien")
    with pytest.raises(ValueError):
        note.generate_waveform()

def test_generate_waveform_with_various_timbres():
    timbres = ["piano", "flute", "harp", "violin"]
    for timbre in timbres:
        note = Note(note_name="A4", timbre=timbre, beat_time=1.0)
        waveform = note.generate_waveform()
        assert isinstance(waveform, np.ndarray)
        assert waveform.shape[0] == int(note.sample_rate * note.duration)

def test_generate_waveform_with_unknown_timbre_raises():
    note = Note(note_name="C4", timbre="unknown_timbre")
    with pytest.raises(ValueError):
        note.generate_waveform()

def test_show_time_and_freq_domain_runs_without_error():
    note = Note(note_name="C4", timbre="flute", beat_time=0.5)
    note.generate_waveform()

    # 捕获标准输出，防止测试时输出混乱
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # 调用绘图函数，确保不抛异常
    note.show_time_and_freq_domain()

    sys.stdout = sys.__stdout__

def test_note_duration_and_volume_edge_cases():
    # 测试duration为0时，是否能正确处理
    note = Note(note_name="C4", beat_time=0)
    waveform = note.generate_waveform()
    assert waveform.size == 0

    # 测试volume边界值
    note = Note(note_name="C4", volume=0)
    waveform = note.generate_waveform()
    assert np.allclose(waveform, 0)

    note = Note(note_name="C4", volume=1)
    waveform = note.generate_waveform()
    assert np.max(np.abs(waveform)) <= 1.0
