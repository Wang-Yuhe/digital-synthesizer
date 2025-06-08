"""Note类测试"""
import pytest
import numpy as np
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
