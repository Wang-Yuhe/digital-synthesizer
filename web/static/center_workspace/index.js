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

// --- 弹窗内播放控制 ---
let playTimer = null;
let playCol = 0;
let isPlaying = false;
let isPaused = false;
let totalCols = 0;
let playBpm = 120;
let playBlockIndex = null;

function resetPlayhead() {
    const playhead = document.getElementById('piano-roll-playhead');
    playhead.style.display = 'none';
    playhead.style.left = '0px';
    // 清除高亮
    document.querySelectorAll('.piano-roll-table td.playing-col').forEach(td => {
        td.classList.remove('playing-col');
    });
    playCol = 0;
    isPlaying = false;
    isPaused = false;
    document.getElementById('modal-playback-status').textContent = '';
}

function movePlayhead(col) {
    const cellWidth = 40;
    const playhead = document.getElementById('piano-roll-playhead');
    playhead.style.display = 'block';
    playhead.style.left = (col * cellWidth) + 'px';

    // 高亮当前列
    document.querySelectorAll('.piano-roll-table tr').forEach(tr => {
        tr.querySelectorAll('td').forEach((td, idx) => {
            if (idx === col) {
                td.classList.add('playing-col');
            } else {
                td.classList.remove('playing-col');
            }
        });
    });
}

function startModalPlayback() {
    if (isPlaying && !isPaused) return;
    isPlaying = true;
    isPaused = false;
    playBpm = parseInt(document.getElementById('modal-bpm-input').value, 10) || 120;
    const barCount = parseInt(document.getElementById('bar-count-range').value, 10) || 8;
    const cellsPerBar = 8;
    totalCols = barCount * cellsPerBar;
    playBlockIndex = parseInt(document.getElementById('modal-title').textContent.replace(/\D/g, ''), 10);

    // 计算每格的间隔（16分音符，BPM=120时每格=0.125s）
    const interval = 60 / playBpm; //1格=1拍

    document.getElementById('modal-playback-status').textContent = '播放中...';

    function step() {
        if (!isPlaying || isPaused) return;
        movePlayhead(playCol);
        playCol++;
        if (playCol >= totalCols) {
            stopModalPlayback();
            return;
        }
        playTimer = setTimeout(step, interval * 1000);
    }
    step();
}

function pauseModalPlayback() {
    isPaused = true;
    document.getElementById('modal-playback-status').textContent = '已暂停';
    if (playTimer) clearTimeout(playTimer);
}

function stopModalPlayback() {
    if (playTimer) clearTimeout(playTimer);
    resetPlayhead();
}

// 绑定弹窗内按钮事件
document.getElementById('modal-play-btn').onclick = function() {
    if (!isPlaying || isPaused) startModalPlayback();
};
document.getElementById('modal-pause-btn').onclick = function() {
    if (isPlaying && !isPaused) pauseModalPlayback();
};
document.getElementById('modal-stop-btn').onclick = function() {
    stopModalPlayback();
};

// 获取输入框元素
const bpmInput = document.getElementById('modal-bpm-input');

// 添加事件监听器，当用户输入时触发
bpmInput.addEventListener('input', function () {
    const newBpm = parseInt(this.value, 10);
    if (!isNaN(newBpm)) {
        playBpm = newBpm;
        console.log('BPM 修改为:', playBpm);
    }
});

// 弹窗关闭时自动复位
document.getElementById('close-modal-btn').addEventListener('click', stopModalPlayback);

/**
 * 显示乐段编辑弹窗，并渲染卷帘格子
 * @param {number} blockIndex 乐段编号
 */
function showNoteBlockModal(blockIndex) {
    resetPlayhead();

    const modal = document.getElementById('note-block-modal');
    modal.style.display = 'flex';
    document.getElementById('modal-title').textContent = `乐段 ${blockIndex} 编辑`;

    // 获取当前小节数（从主页面滑块获取）
    const barCount = parseInt(document.getElementById('bar-count-range').value, 10) || 8;
    // 获取当前BPM（可根据实际情况获取，这里默认120）
    //const bpm = 120;
    //playBpm = parseInt(document.getElementById('modal-bpm-input').value, 10) || 120;
    // 渲染卷帘格子
    renderPianoRoll({ bar_count: barCount , block_index: blockIndex});

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

    // 渲染左侧pitches (table)
    const pitchesDiv = document.getElementById('piano-roll-pitches');
    let pitchTable = '<table class="piano-roll-pitch-table"><tbody>';
    for (let i = 0; i < pitches.length; i++) {
      pitchTable += `<tr><td>${pitches[i]}</td></tr>`;
    }
    pitchTable += '</tbody></table>';
    pitchesDiv.innerHTML = pitchTable;

    // 渲染时间轴
    const timelineDiv = document.getElementById('piano-roll-timeline');
    let timelineHtml = `<table class="piano-roll-timeline-table" style="min-width:${totalCells * cellWidth}px;"><tr>`;
    for (let i = 0; i < totalCells; i++) {
      if (i % cellsPerBar === 0) {
        timelineHtml += `<td colspan="${cellsPerBar}">${i/cellsPerBar+1}</td>`;
      }
    }
    timelineHtml += '</tr></table>';
    timelineDiv.innerHTML = timelineHtml;

    // 渲染钢琴卷帘格子
    const container = document.getElementById('piano-roll-container');
    let gridHtml = `<table class="piano-roll-table" style="min-width:${totalCells * cellWidth}px;"><tbody>`;
    for (let r = 0; r < pitches.length; r++) {
        gridHtml += '<tr>';
        for (let c = 0; c < totalCells; c++) {
            gridHtml += `<td class="piano-cell" data-pitch="${pitches[r]}" data-bar="${c}"></td>`;
        }
        gridHtml += '</tr>';
    }
    gridHtml += '</tbody></table>';
    container.innerHTML = gridHtml;

    // 滚动同步
    const wrapper = document.getElementById('piano-roll-scroll');
    wrapper.addEventListener('scroll', () => {
        document.getElementById('piano-roll-pitches').scrollTop = wrapper.scrollTop;
        document.getElementById('piano-roll-timeline').scrollLeft = wrapper.scrollLeft;
    });


    // 状态变量
    let isDragging = false;
    let dragStartIdx = -1;
    let dragRowCells = [];
    let dragRowElement = null;

    // 工具：清除一个音符片段
    function clearNoteSegment(rowCells, idx) {
        let start = idx;
        while (start > 0 && (rowCells[start].classList.contains('note-body')||rowCells[start].classList.contains('note-tail'))) start--;
        if (!rowCells[start].classList.contains('note-head')) return;
        let end = start;
        while (end + 1 < rowCells.length && (rowCells[end+1].classList.contains('note-body') || rowCells[end+1].classList.contains('note-tail'))) end++;
        for (let i = start; i <= end; i++) {
            rowCells[i].classList.remove('note-head','note-body','note-tail');
        }
        return end-start+1;
    }

    // 阻止右键默认菜单
    const wrapper_r = document.getElementById('piano-roll-scroll');
    wrapper_r.addEventListener('contextmenu', e => e.preventDefault());

    // 注册事件：添加、调整、删除
    container.querySelectorAll('.piano-cell').forEach(cell => {
        cell.addEventListener('mousedown', e => {
            const row = cell.parentElement;
            dragRowElement = row;
            dragRowCells = Array.from(row.querySelectorAll('.piano-cell'));
            dragStartIdx = dragRowCells.indexOf(cell);
            if (e.button === 0) {
                // 左键：新增或开始修改
                isDragging = true;
                if (!cell.classList.contains('note-head')) {
                    clearNoteSegment(dragRowCells, dragStartIdx);
                    cell.classList.add('note-head');
                }
            } else if (e.button === 2) {
                // 右键：删除整段
                clear_len=clearNoteSegment(dragRowCells, dragStartIdx);
                fetch('/note_edit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        pitch: dragRowCells[dragStartIdx].getAttribute('data-pitch'),
                        barIdx: dragStartIdx,
                        length: clear_len,
                        state: 0,
                        block_index: data.block_index,
                        bpm: playBpm,
                    })
                });
            }
        });

        // 鼠标松开时，完成拖动
        cell.addEventListener('mouseup', e => {
            if (!isDragging) return;
            const row = cell.parentElement;
            const rowCells = Array.from(row.querySelectorAll('.piano-cell'));
            const endIdx = rowCells.indexOf(cell);
            if (endIdx > dragStartIdx) {
                for (let i = dragStartIdx + 1; i < endIdx; i++) {
                    rowCells[i].classList.remove('note-tail','note-body','note-head');
                    rowCells[i].classList.add('note-body');
                }
                rowCells[endIdx].classList.remove('note-tail','note-body','note-head')
                rowCells[endIdx].classList.add('note-tail');
            }

            // 拖动扩展音符长度时，直接使用dragStartIdx和endIdx计算长度
            if (endIdx >= dragStartIdx) {
                // 确定音符起始和结束位置
                const start = dragStartIdx;
                const end = endIdx;
                const length = end - start + 1;
                const pitch = rowCells[start].getAttribute('data-pitch');

                // 发送新增/调整长度请求（添加错误处理）
                fetch('/note_edit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        pitch: pitch,
                        barIdx: start,
                        length: length,
                        state: 1, // state=1表示新增/调整
                        block_index: data.block_index,
                        bpm: playBpm,
                    })
                })
                .then(res => {
                    if (!res.ok) throw new Error(`HTTP状态码异常: ${res.status}`);
                    return res.json();
                })
                .then(data => console.log('长度更新成功:', data))
                .catch(err => console.error('长度更新失败:', err));
            }

            isDragging = false;
            dragStartIdx = -1;
            dragRowCells = [];
            dragRowElement = null;
        });
    });

    // 全局监听鼠标松开，保证拖动状态同步
    document.addEventListener('mouseup', function mouseUpHandler(e) {
        if (isDragging) {
            isDragging = false;
            dragStartIdx = -1;
            dragRowCells = [];
            dragRowElement = null;
        }
        // 只需一次，移除监听
        document.removeEventListener('mouseup', mouseUpHandler);
    });

    function getCellState(cell) {
        if (cell.classList.contains('note-head')) return 'head';
        if (cell.classList.contains('note-body')) return 'body';
        if (cell.classList.contains('note-tail')) return 'tail';
        return 'empty';
    }

    // 拖动高亮与消去
    container.addEventListener('mousemove', e => {
        if (!isDragging || dragStartIdx < 0) return;
        const target = e.target.closest('.piano-cell');
        if (!target || target.parentElement !== dragRowElement) {
            // 鼠标移出当前行，立即终止拖动并清除高亮
            if (dragRowCells.length && dragStartIdx >= 0) {
                clearNoteSegment(dragRowCells ,dragStartIdx);
                /*
                for (let i = dragStartIdx; i < dragRowCells.length; i++) {
                    dragRowCells[i].classList.remove('note-head', 'note-body','note-tail');
                }*/
            }
            isDragging = false;
            dragStartIdx = -1;
            dragRowCells = [];
            dragRowElement = null;
            return;
        }
        const idx = dragRowCells.indexOf(target);
        // 先当前建的body/tail，实时拖拽
        for (let i = dragStartIdx+1; i < dragRowCells.length; i++) {
            if(getCellState(dragRowCells[i])=="empty")break;
            dragRowCells[i].classList.remove('note-body','note-tail');
        }
        if (idx > dragStartIdx) {
            // 向右拖动：高亮body和tail
            for (let i = dragStartIdx + 1; i < idx; i++) {
                dragRowCells[i].classList.add('note-body');
            }
            dragRowCells[idx].classList.add('note-tail');
        } else {
            // 向左回退：只保留head，实时消去body/tail
            // 已在上面清理
        }
    });
}


// --------- 样式动态注入（如已在全局CSS中可省略） ---------
const style = document.createElement('style');
style.textContent = `
.piano-roll-table { border-collapse: collapse; width: 100%; }
.piano-roll-table td { border: 1px solid #888; width: 32px; height: 28px; background: #666; }
.piano-roll-table .pitch-label { background: #333; color: #fff; width: 32px; text-align: center; }
.piano-roll-table .piano-cell.active { background: #4fc3f7; }
/* 新增样式：隐藏格子线 */
.piano-roll-table .no-border {
    border-left: none;
}
.piano-roll-table .note-head.no-border {
    border-left: 1px solid #888;
}
`;
document.head.appendChild(style);