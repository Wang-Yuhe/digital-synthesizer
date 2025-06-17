from flask import Flask, render_template, request, jsonify, g
from src.note_block import NoteBlock
import sounddevice as sd

app = Flask(__name__)

audio_samples = {
    "Bass": ["bass_loop_01.wav", "bass_loop_02.wav"],
    "Drums": ["drum_beat_01.wav", "drum_beat_02.wav"],
    "Guitars": ["guitar_riff_01.wav"],
}

note_blocks = []  # NoteBlock 列表
current_nb = None  # 当前播放的 NoteBlock

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
    nb = NoteBlock(timbre="piano",
                   note_names=["C4", "E4"],
                   beat_times=[1, 2],
                   volume=[0.8, 0.6],
                   start_beat=[0, 1])

    note_blocks.append(nb)
    global current_nb,current_nb_id
    current_nb = nb
    length = nb.generate_waveform()
    # 返回所有乐段索引，用于前端刷新显示
    note_blocks_info = [{"index": i+1} for i in range(len(note_blocks))]
    return jsonify({"length": length.tolist(), "note_blocks": note_blocks_info})

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


if __name__ == '__main__':
    app.run(debug=True)
