import numpy as np
from src.track import Track

def test_add_note_block():
    track = Track()
    success = track.add_note_block(["C4", "E4"], [1, 2], [0.8, 0.6], [0, 1])
    assert success is True
    assert len(track.note_blocks) == 1
    nb = track.note_blocks[0]
    assert nb.note_names == ["C4", "E4"]
    assert nb.beat_times == [1, 2]
    assert nb.start_beat == [0, 1]

def test_remove_note_block():
    track = Track()
    track.add_note_block(["C4"], [1])
    track.add_note_block(["D4"], [1])
    assert len(track.note_blocks) == 2

    removed = track.remove_note_block(0)
    assert removed is True
    assert len(track.note_blocks) == 1
    assert track.note_blocks[0].block_id == 0

    fail = track.remove_note_block(10)
    assert fail is False

def test_generate_waveform():
    track = Track()
    track.add_note_block(["C4", "E4"], [1, 1])
    waveform = track.generate_waveform()
    assert waveform is not None
    assert isinstance(waveform, np.ndarray)
    assert waveform.size > 0

def test_calculate_pitch_range():
    track = Track()
    track.add_note_block(["C4", "G4", "E4"], [1, 1, 1])
    track.generate_waveform()
    pitch_range = track.calculate_pitch_range()
    assert pitch_range == "C4-G4"

def test_empty_pitch_range():
    track = Track()
    pitch_range = track.calculate_pitch_range()
    assert pitch_range == "No notes in track"
