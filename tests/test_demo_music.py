import numpy as np
from src.digital_synthesizer import DigitalSynthesizer
from src.track import Track
from src.demo_music import music1, music2

def test_music1_structure():
    melody, accompaniment = music1()
    assert isinstance(melody, Track)
    assert isinstance(accompaniment, Track)
    assert len(melody.note_blocks) > 0
    assert len(accompaniment.note_blocks) > 0

def test_music2_structure():
    melody, accompaniment = music2()
    assert isinstance(melody, Track)
    assert isinstance(accompaniment, Track)
    assert len(melody.note_blocks) > 0
    assert len(accompaniment.note_blocks) > 0

def test_synthesizer_generate_waveform():
    melody, accompaniment = music1()
    synth = DigitalSynthesizer(volume=0.2)
    synth.add_track(melody)
    synth.add_track(accompaniment)

    waveform = synth.generate_waveform()
    assert waveform is not None
    assert isinstance(waveform, np.ndarray)
    assert all(isinstance(x, float) for x in waveform)

# 可选：模拟播放和保存（推荐mock）
def test_synthesizer_mock_play_save(mocker):
    synth = DigitalSynthesizer()
    mocker.patch.object(synth, 'play_for_preview')
    mocker.patch.object(synth, 'save_to_file')

    melody, accompaniment = music2()
    synth.add_track(melody)
    synth.add_track(accompaniment)
    synth.generate_waveform()

    synth.play_for_preview()
    synth.save_to_file("testfile")

    synth.play_for_preview.assert_called_once()
    synth.save_to_file.assert_called_once_with("testfile")
