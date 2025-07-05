from flask import Flask, render_template, request, jsonify, g
from src.note_block import NoteBlock
from src.track import Track
from src.digital_synthesizer import DigitalSynthesizer
from src.note import Note
from web.save import note_saver, track_saver
import sounddevice as sd

app = Flask(__name__)

audio_samples = {
    "Bass": ["bass_loop_01.wav", "bass_loop_02.wav"],
    "Drums": ["drum_beat_01.wav", "drum_beat_02.wav"],
    "Guitars": ["guitar_riff_01.wav"],
}

note_blocks = []  # NoteBlock 列表
current_nb = None  # 当前播放的 NoteBlock
digital_synthesizer = DigitalSynthesizer()  # 数字合成器实例

@app.route('/')

def index():
    categories = list(audio_samples.keys())

    # 传递 note_blocks 的简化信息给模板
    nb_infos = [{"index": i, "timbre": nb.timbre} for i, nb in enumerate(note_blocks)]

    return render_template('index.html', categories=categories, note_blocks=nb_infos)

# 获取所有乐段（供 JS 动态更新）
@app.route('/get_note_blocks', methods=['GET'])
def get_note_blocks():
    note_blocks_info = [{"index": i + 1} for i in range(len(note_blocks))]
    return jsonify({
        "length": len(note_blocks),
        "note_blocks": note_blocks_info
    })

@app.route('/add_track', methods=['POST'])
def add_track():
    nb = track_saver(timbre="piano", track_id=len(note_blocks))

    note_blocks.append(nb)
    global current_nb,current_nb_id
    current_nb = nb
    #length = nb.generate_waveform()
    # 返回所有乐段索引，用于前端刷新显示
    note_blocks_info = [{"index": i+1} for i in range(len(note_blocks))]
    return jsonify({"note_blocks": note_blocks_info})

@app.route('/set_current_nb', methods=['POST'])
def set_current_nb():
    global current_nb
    index = request.json.get("index")

    if index >= 0 and index < len(note_blocks):
        current_nb = note_blocks[index]
        return jsonify({"status": "success", "message": f"Current NoteBlock set to index {index}"})
    else:
        return jsonify({"status": "error", "message": "Invalid index"}), 400

@app.route('/play', methods=['POST'])
def play():
    if current_nb:
        waveform = current_nb.generate_waveform()
        sd.play(waveform, samplerate=current_nb.sample_rate)
        return jsonify({"status": "success", "message": "Playing current NoteBlock"})
    else:
        return jsonify({"status": "error", "message": "No NoteBlock selected"}), 400

@app.route('/note_edit', methods=['POST'])
def note_edit():
    data = request.get_json()
    state = data.get('state')# 0表示删除，1表示增加
    pitch = data.get('pitch')
    bar_idx = data.get('barIdx')
    length = data.get('length')
    block_index = data.get('block_index')
    bpm = data.get('bpm')
    # bar_idx 0开始的
    #print(f"bpm:{bpm} ")
    if state==1:
        # bug:连续点击会导致崩溃
        now_note=Note(note_name=pitch, beat_time=1, bpm=bpm)
        now_note.generate_waveform()
        now_note.play_for_preview()
        print(f"收到音符块: pitch={pitch}, barIdx={bar_idx}, length={length}, blockIndex={block_index}")
    else:
        print(f"删除音符块: pitch={pitch}, barIdx={bar_idx}, length={length}, blockIndex={block_index}")  
    
    return jsonify({"status": "success", "message": "Note block received", "data": data})

if __name__ == '__main__':
    app.run(debug=True)
