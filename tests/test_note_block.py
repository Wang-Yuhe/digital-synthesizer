import numpy as np
import pytest
import io
import sys
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

def test_show_time_domain_runs_without_error():
    nb = NoteBlock(timbre="piano",
                   note_names=["C4", "E4"],
                   beat_times=[1, 2],
                   volume=[0.8, 0.6],
                   start_beat=[0, 1])
    nb.generate_waveform()

    captured_output = io.StringIO()
    sys.stdout = captured_output

    # 调用show_time_domain，确保不抛异常
    nb.show_time_domain()

    sys.stdout = sys.__stdout__

def test_empty_noteblock_behavior():
    nb = NoteBlock(note_names=[])
    # 没有音符时，生成波形应返回空或长度0数组
    waveform = nb.generate_waveform()
    assert isinstance(waveform, np.ndarray)
    assert waveform.size == 0 or np.all(waveform == 0)

    # show_time_domain 也应安全调用
    nb.show_time_domain()

def test_add_note_invalid_inputs():
    nb = NoteBlock()
    # 测试添加非法参数是否抛出异常
    with pytest.raises(TypeError):
        nb.add_note(123, "wrong_type", -1, "volume")

def test_waveform_amplitude_and_overlap():
    # 两个音符重叠，验证叠加波形幅度是否合理
    nb = NoteBlock(timbre="piano",
                   note_names=["C4", "C4"],
                   beat_times=[1, 1],
                   volume=[0.5, 0.5],
                   start_beat=[0, 0])  # 同时开始

    waveform = nb.generate_waveform()
    assert np.max(np.abs(waveform)) <= 1.0  # 不超出正常幅度范围
    assert waveform.size > 0
