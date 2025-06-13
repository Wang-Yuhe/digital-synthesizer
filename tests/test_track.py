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

def test_add_note_block_autofill_params():
    track = Track()
    success = track.add_note_block(["C4", "E4", "G4"], [1, 1, 1], volume=[0.7], start_beat=[0.5])
    assert success is True
    nb = track.note_blocks[0]
    assert nb.volume == [0.7, 1, 1]
    assert nb.start_beat == [0.5, 0, 0]

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

def test_block_id_reset_after_remove():
    track = Track()
    track.add_note_block(["C4"], [1])
    track.add_note_block(["D4"], [1])
    track.add_note_block(["E4"], [1])
    track.remove_note_block(1)
    assert [nb.block_id for nb in track.note_blocks] == [0, 1]

def test_generate_waveform():
    track = Track()
    track.add_note_block(["C4", "E4"], [1, 1])
    waveform = track.generate_waveform()
    assert waveform is not None
    assert isinstance(waveform, np.ndarray)
    assert waveform.size > 0

def test_generate_waveform_empty_track():
    track = Track()
    waveform = track.generate_waveform()
    assert isinstance(waveform, np.ndarray)
    assert waveform.size == 0

def test_calculate_pitch_range():
    track = Track()
    track.add_note_block(["C4", "G4", "E4"], [1, 1, 1])
    track.generate_waveform()
    pitch_range = track.calculate_pitch_range()
    assert pitch_range == "C4-G4"

def test_pitch_range_with_rest_note():
    track = Track()
    track.add_note_block(["rest", "C4", "E4"], [1, 1, 1])
    pitch_range = track.calculate_pitch_range()
    assert pitch_range == "C4-E4"

def test_empty_pitch_range():
    track = Track()
    pitch_range = track.calculate_pitch_range()
    assert pitch_range == "No notes in track"

def test_change_timbre():
    track = Track("piano")
    track.add_note_block(["C4"], [1])
    success = track.change_timbre("flute")
    assert success is True
    assert track.timbre == "flute"
    assert all(nb.timbre == "flute" for nb in track.note_blocks)
    success = track.change_timbre("flute")
    assert success is False
