from flask import Flask, render_template, request, jsonify, g
from src.note_block import NoteBlock
from src.track import Track
from src.digital_synthesizer import DigitalSynthesizer
from src.note import Note
from web.save import note_saver, track_saver
from web.play import play_numpy_waveform,stop_waveform_playback
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
        play_numpy_waveform(now_note.waveform)
        print(f"收到音符块: pitch={pitch}, barIdx={bar_idx}, length={length}, blockIndex={block_index}")
    else:
        print(f"删除音符块: pitch={pitch}, barIdx={bar_idx}, length={length}, blockIndex={block_index}")  
    
    return jsonify({"status": "success", "message": "Note block received", "data": data})

@app.route('/save_note_block', methods=['POST'])
def save_note_block():
    data = request.get_json()
    notes = data.get('notes', [])
    # 这里可以保存到数据库、文件，或更新内存结构
    """
    print(f"收到批量音符，共{len(notes)}条")
    for note in notes:
        print(note)
    """
    # TODO: 实际保存逻辑
    if notes:
        block_index = notes[0].get('block_index')
        print(block_index)
        now_track = track_saver(
            #timbre=notes[0].get('timbre', 'piano'),#到时候可选的
            bpm=notes[0].get('bpm'),
            track_id=block_index,
        )
        for note in notes:
            now_note=note_saver(
                note_name=note.get('pitch'),
                length=note.get('length'),
                bar_idx=note.get('barIdx'),
            )
            now_track.add_note(now_note)
        if block_index<=len(note_blocks):
            note_blocks[block_index-1] = now_track  # 更新对应的 NoteBlock
        else:
            return jsonify({"status": "error", "message": "保存失败"}), 400

        for i in note_blocks:
            print(f"乐段 {i.track_id} 的音符信息: {i.get_note_information()}")

    return jsonify({"status": "success", "message": f"已保存{len(notes)}个音符"})

@app.route('/get_note_block_details', methods=['GET'])
def get_note_block_details():
    block_index = request.args.get('block_index', type=int)
    if block_index is None or block_index < 1 or block_index > len(note_blocks):
        return jsonify({"status": "error", "message": "无效的乐段编号"}), 400
    
    # 从 note_blocks 中获取对应乐段的音符数据
    track = note_blocks[block_index - 1]
    notes = []
    for note_saver in track.note_savers:
        note_info = note_saver.get_information()
        notes.append({
            "pitch": note_info[0],       # 音高（如 "C4"）
            "barIdx": note_info[2],      # 起始小节位置（barIdx）
            "length": note_info[1]       # 音符长度（占用的格子数）
        })
    
    return jsonify({
        "status": "success",
        "notes": notes,
        "bpm": track.bpm                # 同步保存的BPM
    })


@app.route('/start_playback', methods=['POST'])
def start_playback():
    global current_playback, current_nb
    data = request.get_json()
    block_index = data.get('block_index')
    start_col = data.get('start_col')
    bpm = data.get('bpm')
    #print(f"{start_col}")

    # 校验乐段编号
    if block_index is None or block_index < 1 or block_index > len(note_blocks):
        return jsonify({"status": "error", "message": "无效的乐段编号"}), 400

    # 获取目标乐段
    current_nb = note_blocks[block_index - 1]
    #current_nb.bpm = bpm  # 更新乐段BPM（可选）
    note_name=[]
    beat_times=[]
    start_beat=[]
    volume=[]
    for i in current_nb.note_savers:
        if i.bar_idx<start_col:continue
        note_name.append(i.note_name)
        beat_times.append(i.length)
        #print(i.bar_idx,start_col)
        start_beat.append(i.bar_idx-start_col)
        volume.append(i.volume)

    #print(current_nb.bpm)
    newblock = NoteBlock(timbre=current_nb.timbre, bpm=current_nb.bpm,
                          note_names=note_name, beat_times=beat_times,
                          start_beat=start_beat, volume=volume)

    # 生成从start_col开始的音频数据（需根据业务逻辑实现）
    waveform = newblock.generate_waveform()

    """
    # 停止之前的播放（如果有）
    if current_playback is not None:
        current_playback.stop()

    # 开始新的播放
    current_playback = sd.OutputStream(samplerate=newblock.sample_rate, channels=1)
    current_playback.start()
    waveform = waveform.astype('float32')
    current_playback.write(waveform)
    #current_playback = sd.play(waveform, samplerate=newblock.sample_rate)
    """
    play_numpy_waveform(waveform)
    return jsonify({"status": "success", "message": "开始播放"})

@app.route('/pause_playback', methods=['POST'])
def pause_playback():
    """
    global current_playback
    if current_playback is not None:
        current_playback.stop()  # 停止当前播放
        current_playback = None
    """
    stop_waveform_playback()
    return jsonify({"status": "success", "message": "已暂停播放"})

@app.route('/stop_playback', methods=['POST'])
def stop_playback():
    """
    global current_playback
    if current_playback is not None:
        current_playback.stop()  # 停止当前播放
        current_playback = None
    """
    stop_waveform_playback()
    return jsonify({"status": "success", "message": "已停止播放"})

if __name__ == '__main__':
    app.run(debug=True)
