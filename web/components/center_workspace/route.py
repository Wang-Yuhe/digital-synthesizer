from flask import Blueprint, render_template, jsonify, request
from src.note_block import NoteBlock
import sounddevice as sd

left_panel_bp = Blueprint('left_panel', __name__,
                          template_folder='templates',
                          static_folder='static')

note_blocks = []
current_nb = None

@left_panel_bp.route('/')
def left_panel():
    # 不传数据，模板内使用ajax加载
    return render_template('index.html')

@left_panel_bp.route('/add_track', methods=['POST'])
def add_track():
    global current_nb
    nb = NoteBlock(timbre="piano",
                   note_names=["C4", "E4"],
                   beat_times=[1, 2],
                   volume=[0.8, 0.6],
                   start_beat=[0, 1])
    note_blocks.append(nb)
    current_nb = nb
    length = nb.generate_waveform()
    note_blocks_info = [{"index": i+1, "timbre": nb.timbre} for i, nb in enumerate(note_blocks)]
    return jsonify({"length": length.tolist(), "note_blocks": note_blocks_info})

@left_panel_bp.route('/get_note_blocks', methods=['GET'])
def get_note_blocks():
    note_blocks_info = [{"index": i+1, "timbre": nb.timbre} for i, nb in enumerate(note_blocks)]
    return jsonify({"length": len(note_blocks), "note_blocks": note_blocks_info})

@left_panel_bp.route('/set_current_nb', methods=['POST'])
def set_current_nb():
    global current_nb
    index = request.json.get("index")
    if 0 <= index < len(note_blocks):
        current_nb = note_blocks[index]
        return jsonify({"status": "success", "message": f"Current NoteBlock set to index {index}"})
    else:
        return jsonify({"status": "error", "message": "Invalid index"}), 400

@left_panel_bp.route('/play', methods=['POST'])
def play():
    if current_nb:
        waveform = current_nb.generate_waveform()
        sd.play(waveform, samplerate=current_nb.sample_rate)
        return jsonify({"status": "success", "message": "Playing current NoteBlock"})
    else:
        return jsonify({"status": "error", "message": "No NoteBlock selected"}), 400
