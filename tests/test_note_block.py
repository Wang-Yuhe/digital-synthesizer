import numpy as np
from src.note_block import NoteBlock

def test_add_and_remove_note():
    nb = NoteBlock(timbre="piano", note_names=["C4"], beat_times=[1], volume=[1], start_beat=[0])
    assert len(nb.notes) == 1
    assert nb.note_names == ["C4"]

    # 添加音符
    nb.add_note("E4", 2, 0.5, 1)
    assert len(nb.notes) == 2
    assert nb.note_names == ["C4", "E4"]

    # 删除音符
    success = nb.remove_note(0)
    assert success is True
    assert len(nb.notes) == 1
    assert nb.note_names == ["E4"]

    # 删除不存在的id
    fail = nb.remove_note(10)
    assert fail is False

def test_generate_waveform_length():
    nb = NoteBlock(timbre="piano",
                   note_names=["C4", "E4"],
                   beat_times=[1, 2],
                   volume=[0.8, 0.6],
                   start_beat=[0, 1])
    waveform = nb.generate_waveform()
    # 波形长度应该和最长的note wave长度一致
    max_len = max(len(note.waveform) for note in nb.notes)
    assert len(waveform) == max_len

def test_waveform_not_empty_after_generation():
    nb = NoteBlock()
    nb.generate_waveform()
    assert nb.waveform is not None
    assert isinstance(nb.waveform, np.ndarray)
    assert nb.waveform.size > 0
