// ================= 中间主工作区 =================

function renderTimeline(barCount) {
    const timeline = document.getElementById('timeline-bar');
    timeline.innerHTML = '';
    for (let i = 1; i <= barCount; i++) {
        const div = document.createElement('div');
        div.textContent = `第${i}小节`;
        timeline.appendChild(div);
    }
    // 动态调整编辑区宽度
    adjustEditAreaWidth(barCount);
}

function adjustEditAreaWidth(barCount) {
    // 70px为每小节宽度，12px为gap，内容区左右有padding
    const minWidth = barCount * 70 + (barCount - 1) * 12 + 32;
    const editArea = document.getElementById('edit-area-content');
    editArea.style.width = minWidth + 'px';
}

document.addEventListener("DOMContentLoaded", function() {
    const barRange = document.getElementById('bar-count-range');
    const barValue = document.getElementById('bar-count-value');
    let barCount = parseInt(barRange.value, 10);

    renderTimeline(barCount);
    barValue.textContent = barCount;

    barRange.addEventListener('input', function() {
        barCount = parseInt(this.value, 10);
        renderTimeline(barCount);
        barValue.textContent = barCount;
    });

    // 你原有的乐段加载逻辑
    loadNoteBlocks();

    // 监听乐段块点击，弹出卷帘窗口
    document.getElementById('note-block-container').addEventListener('click', function(e) {
        const item = e.target.closest('.note-block-item');
        if (item) {
            // 获取乐段编号（这里用下标+1，实际可根据你的数据结构调整）
            const index = Array.from(document.querySelectorAll('.note-block-item')).indexOf(item);
            openNoteBlockEditor(index + 1);
        }
    });
});

// 加载并渲染乐段（note_blocks）
function loadNoteBlocks() {
    fetch('/get_note_blocks')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('note-block-container');
            container.innerHTML = '';
            if (data.note_blocks.length === 0) {
                container.innerHTML = `<div class="empty-segment-placeholder">
                    在这里添加循环乐段或双击创建片段
                </div>`;
            } else {
                const list = document.createElement('div');
                list.className = 'note-block-list';
                data.note_blocks.forEach(block => {
                    const div = document.createElement('div');
                    div.className = 'note-block-item';
                    div.textContent = `乐段 #${block.index}`;
                    list.appendChild(div);
                });
                container.appendChild(list);
            }
        })
        .catch(error => {
            console.error("加载乐段失败：", error);
        });
}

// 渲染note_blocks列表的函数（可用于局部刷新）
function renderNoteBlocks(noteBlocks) {
    const container = document.querySelector('.note-block-list');
    if (!container) return;

    if (noteBlocks.length === 0) {
        container.innerHTML = `<div class="empty-segment-placeholder">
            在这里添加循环乐段或双击创建片段
        </div>`;
    } else {
        container.innerHTML = noteBlocks.map(nb => `
            <div class="note-block-item p-2 rounded" style="background-color:#333; cursor:pointer;">
                <strong>声轨 ${nb.index + 1}</strong> - 音色: ${nb.timbre}
            </div>
        `).join('');
    }
}

// 播放按钮事件
document.getElementById('play-btn').addEventListener('click', () => {
    fetch('/play', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
        })
        .catch(err => {
            console.error(err);
            alert('播放失败');
        });
});

/**
 * 打开乐段编辑弹窗（卷帘窗口）
 * @param {number} blockIndex 乐段编号
 */
function openNoteBlockEditor(blockIndex) {
    showNoteBlockModal(blockIndex);
}

/**
 * 显示乐段编辑弹窗，并渲染卷帘格子
 * @param {number} blockIndex 乐段编号
 */
function showNoteBlockModal(blockIndex) {
    const modal = document.getElementById('note-block-modal');
    modal.style.display = 'flex';
    document.getElementById('modal-title').textContent = `乐段 #${blockIndex} 编辑`;

    // 获取当前小节数（从主页面滑块获取）
    const barCount = parseInt(document.getElementById('bar-count-range').value, 10) || 8;
    // 获取当前BPM（可根据实际情况获取，这里默认120）
    //const bpm = 120;
    //document.getElementById('modal-bpm-input').value = bpm;

    // 渲染卷帘格子
    renderPianoRoll({ bar_count: barCount });
}

// 关闭弹窗
document.getElementById('close-modal-btn').onclick = () => {
    document.getElementById('note-block-modal').style.display = 'none';
};

/**
 * 渲染钢琴卷帘格子
 * @param {Object} data - 包含 bar_count 等参数
 */
function renderPianoRoll(data) {
    // 参数
    const barCount = data.bar_count || 8;
    const cellsPerBar = 8;
    const totalCells = barCount * cellsPerBar;
    const cellWidth = 40;
    const pitches = [];
    const pitchNames = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
    for (let octave = 2; octave <= 6; octave++) {
        for (const note of pitchNames) {
            pitches.push(`${note}${octave}`);
        }
    }

    // 1. 渲染左侧pitches
    const pitchesDiv = document.getElementById('piano-roll-pitches');
    pitchesDiv.innerHTML = '';
    for (let i = pitches.length - 1; i >= 0; i--) {
        const label = document.createElement('div');
        label.className = 'piano-roll-pitch-label';
        label.textContent = pitches[i];
        pitchesDiv.appendChild(label);
    }

    // 2. 渲染时间轴
    const timelineDiv = document.getElementById('piano-roll-timeline');
    let timelineHtml = `<table class="piano-roll-timeline-table" style="min-width:${totalCells * cellWidth}px;"><tr>`;
    for (let i = 0; i < totalCells; i++) {
        if (i % cellsPerBar === 0) {
            timelineHtml += `<td colspan="${cellsPerBar}">${i/cellsPerBar+1}</td>`;
        }
    }
    timelineHtml += '</tr></table>';
    timelineDiv.innerHTML = timelineHtml;

    // 3. 渲染卷帘格子
    const container = document.getElementById('piano-roll-container');
    let html = `<table class="piano-roll-table" style="min-width:${totalCells * cellWidth}px;"><tbody>`;
    for (let p = pitches.length - 1; p >= 0; p--) {
        html += '<tr>';
        for (let b = 0; b < totalCells; b++) {
            html += `<td class="piano-cell" data-pitch="${pitches[p]}" data-bar="${b}"></td>`;
        }
        html += '</tr>';
    }
    html += '</tbody></table>';
    container.innerHTML = html;

    // 4. 音符延长功能
    let isDragging = false;
    let dragStartCell = null;
    let dragRowCells = [];
    let dragStartIdx = -1;

    // 鼠标按下：准备延长音符
    container.querySelectorAll('.piano-cell').forEach(cell => {
        cell.addEventListener('mousedown', function(e) {
            if (e.button !== 0) return; // 只响应左键
            isDragging = true;
            dragStartCell = this;
            const row = this.parentElement;
            dragRowCells = Array.from(row.querySelectorAll('.piano-cell'));
            dragStartIdx = dragRowCells.indexOf(this);
            // 清除本行所有note-head/note-body/note-tail
            dragRowCells.forEach(c => c.classList.remove('note-head', 'note-body', 'note-tail'));
            // 先激活起点
            this.classList.add('note-head');
        });
    });

    // 鼠标移动：高亮延长范围
    container.addEventListener('mousemove', function(e) {
        if (!isDragging || !dragStartCell) return;
        const target = e.target.closest('.piano-cell');
        if (!target || target.parentElement !== dragStartCell.parentElement) return;
        const idx = dragRowCells.indexOf(target);
        if (idx < 0) return;
        // 清除
        dragRowCells.forEach(c => c.classList.remove('note-body', 'note-tail', 'dragging'));
        // 头到当前格全部高亮
        if (idx > dragStartIdx) {
            for (let i = dragStartIdx + 1; i <= idx; i++) {
                dragRowCells[i].classList.add('note-body');
            }
            dragRowCells[idx].classList.add('note-tail');
        }
        // 拖动时高亮边框
        target.classList.add('dragging');
    });

    // 鼠标松开：确定音符长度
    container.addEventListener('mouseup', function(e) {
        if (!isDragging || !dragStartCell) return;
        isDragging = false;
        dragRowCells.forEach(c => c.classList.remove('dragging'));
        dragStartCell = null;
        dragRowCells = [];
        dragStartIdx = -1;
    });

    // 单击cell：新建/取消音符
    container.querySelectorAll('.piano-cell').forEach(cell => {
        cell.addEventListener('click', function(e) {
            if (isDragging) return;
            // 如果是音符头，点击取消
            if (this.classList.contains('note-head')) {
                this.classList.remove('note-head');
                // 同行后续body和tail也取消
                let next = this.nextElementSibling;
                while (next && (next.classList.contains('note-body') || next.classList.contains('note-tail'))) {
                    next.classList.remove('note-body', 'note-tail');
                    next = next.nextElementSibling;
                }
            } else {
                // 新建音符
                this.classList.add('note-head');
            }
        });
    });
}


// --------- 样式动态注入（如已在全局CSS中可省略） ---------
const style = document.createElement('style');
style.textContent = `
.piano-roll-table { border-collapse: collapse; width: 100%; }
.piano-roll-table td { border: 1px solid #888; width: 32px; height: 28px; background: #666; }
.piano-roll-table .pitch-label { background: #333; color: #fff; width: 32px; text-align: center; }
.piano-roll-table .piano-cell.active { background: #4fc3f7; }
`;
document.head.appendChild(style);