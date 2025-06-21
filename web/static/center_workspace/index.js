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
    const bpm = 120;
    document.getElementById('modal-bpm-input').value = bpm;

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
    const container = document.getElementById('piano-roll-container');
    container.innerHTML = ''; // 清空旧内容

    // 八度音阶（可根据需要调整）
    const pitches = ['C', 'B', 'A', 'G', 'F', 'E', 'D', 'C'];
    const barCount = data.bar_count || 8;

    // 每个小节宽度（与主界面时间线一致）
    const cellWidth = 70; // px

    // 构建表格HTML，并设置宽度
    let html = `<div style="overflow-x:auto;">
        <table class="piano-roll-table" style="min-width:${barCount * cellWidth + 40}px;">
        <tbody>`;
    for (let p = 0; p < pitches.length; p++) {
        html += '<tr>';
        html += `<td class="pitch-label">${pitches[p]}</td>`;
        for (let b = 0; b < barCount; b++) {
            html += `<td class="piano-cell" data-pitch="${pitches[p]}" data-bar="${b}"></td>`;
        }
        html += '</tr>';
    }
    html += '</tbody></table></div>';
    container.innerHTML = html;

    // 可选：为每个格子添加点击事件，实现激活/取消激活效果
    container.querySelectorAll('.piano-cell').forEach(cell => {
        cell.addEventListener('click', function() {
            this.classList.toggle('active');
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