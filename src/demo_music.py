"""用以展示部分后端功能"""
from src.digital_synthesizer import DigitalSynthesizer
from src.track import Track

def music1(timbre="piano"):
    """展示乐段1，生日歌"""
    # 旋律音轨
    melody1 = Track(timbre=timbre)
    melody1.add_note_block("C4,C4,D4,C4,F4,E4".split(","), [0.5, 0.5, 1, 1, 1, 2], start_beat=[0, 0.5, 1, 2, 3, 4])
    melody1.add_note_block("C4,C4,D4,C4,G4,F4".split(","), [0.5, 0.5, 1, 1, 1, 2], start_beat=[0, 0.5, 1, 2, 3, 4])
    melody1.add_note_block("C4,C4,C5,A4,F4,E4,D4".split(","), [0.5, 0.5, 1, 1, 1, 1, 1], start_beat=[0, 0.5, 1, 2, 3, 4, 5])
    melody1.add_note_block("Bb4,Bb4,A4,F4,G4,F4".split(","), [0.5, 0.5, 1, 1, 1, 2], start_beat=[0, 0.5, 1, 2, 3, 4])

    accompaniment1 = Track(timbre=timbre)
    accompaniment1.add_note_block("F2,C3,G2,E3".split(","),[2,2,2,2],start_beat=[1,1,4,4])
    accompaniment1.add_note_block("E2,C3,F2,C3".split(","),[2,2,2,2],start_beat=[1,1,4,4])
    accompaniment1.add_note_block("F2,C3,G2,D3".split(","),[2,2,2,2],start_beat=[1,1,4,4])
    accompaniment1.add_note_block("F2,A2,G2,C3,F2,C3".split(","),[2,2,1,1,1,1],start_beat=[1,1,3,3,4,4])

    return melody1, accompaniment1

def music2(timbre="piano"):
    """展示乐段2"""
    melody1 = Track(timbre=timbre)
    melody1.add_note_block(["E4","F#4","G#4","G#4","F#4","E4","E4"],[1,0.5,0.5,0.5,0.5,0.5,0.5],start_beat=[0,1,1.5,2,2.5,3,3.5])
    accompaniment1 = Track(timbre=timbre)
    accompaniment1.add_note_block("A1,A2,E3,A3,A1,A2,E3,A3".split(","),[2,2,1,1,1,1,1,1],start_beat=[0,0,1,1,2,2,3,3])

    melody1.add_note_block(["F#4","G#4","F#4","E4","E4","E4"],[1,1,0.5,0.5,0.5,0.5],start_beat=[0,1,2,2.5,3,3.5])
    accompaniment1.add_note_block(["G#1","G#2","E3","G#3","G#1","G#2","E3","G#3"],[2,2,1,1,1,1,1,1],start_beat=[0,0,1,1,2,2,3,3])

    melody1.add_note_block(["F#4","G#4","F#4","G#4"],[1,1,1,1],start_beat=[0,1,2,3])
    accompaniment1.add_note_block(["C#1","C#2","E3","G#3","C#1","C#2","E3","G#3"],[2,2,1,1,1,1,1,1],start_beat=[0,0,1,1,2,2,3,3])

    melody1.add_note_block(["E4","B4","E4","A4","G#4","F#4"],[0.5,0.5,0.5,0.5,0.5,1],start_beat=[0,0.5,1.5,2,2.5,3])
    accompaniment1.add_note_block(["B1","B2","B3","G#3","B1","B2","B3","G#3"],[2,2,1,1,1,1,1,1],start_beat=[0,0,1,1,2,2,3,3])

    return melody1, accompaniment1

if __name__=="__main__":
    synthesizer = DigitalSynthesizer(volume=0.5)
    melody, accompaniment=music1(timbre="piano")
    #melody, accompaniment=music2()

    synthesizer.add_track(melody)
    synthesizer.add_track(accompaniment)
    synthesizer.generate_waveform()
    synthesizer.play_for_preview()
    #synthesizer.save_to_file('piccolo')
