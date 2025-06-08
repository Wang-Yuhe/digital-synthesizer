import numpy as np
from src.digital_synthesizer import DigitalSynthesizer
from src.track import Track

def test_add_and_remove_track():
    synth = DigitalSynthesizer()
    track1 = Track(timbre="piano")
    track2 = Track(timbre="violin")

    synth.add_track(track1)
    synth.add_track(track2)

    assert len(synth.tracks) == 2
    assert synth.tracks[0].timbre == "piano"
    assert synth.tracks[1].timbre == "violin"

    synth.remove_track(0)
    assert len(synth.tracks) == 1
    assert synth.tracks[0].timbre == "violin"
    assert synth.tracks[0].track_id == 0  # 重新编号是否正确

def test_add_track_by_property():
    synth = DigitalSynthesizer()
    track = synth.add_track_by_property(timbre="flute", pitch_range="C4-B5", bpm=120, sample_rate=44100, volume=0.8)
    assert len(synth.tracks) == 1
    assert track.timbre == "flute"
    assert track.volume == 0.8

def test_generate_waveform():
    synth = DigitalSynthesizer(volume=0.5)
    track = Track(timbre="piano")
    track.add_note_block(["C4", "E4", "G4"], [1, 1, 2])
    synth.add_track(track)

    waveform = synth.generate_waveform()
    assert isinstance(waveform, np.ndarray)
    assert waveform.ndim == 1
    assert len(waveform) > 0
    assert synth.waveform is not None

def test_set_bpm():
    synth = DigitalSynthesizer()
    synth.set_bpm(150)
    assert synth.bpm == 150

def test_remove_track_invalid_id():
    synth = DigitalSynthesizer()
    result = synth.remove_track(0)  # 没有轨道，删除应失败
    assert result is False
