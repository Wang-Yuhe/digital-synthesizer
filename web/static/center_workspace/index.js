// ================= 中间主工作区 =================
// 加载并渲染乐段（note_blocks）
function loadNoteBlocks() {
    fetch('/get_note_blocks')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('note-block-container');
            container.innerHTML = '';
            data.note_blocks.forEach(block => {
                const div = document.createElement('div');
                div.className = 'note-block-item';
                div.textContent = `乐段 #${block.index}`;
                container.appendChild(div);
            });
        })
        .catch(error => {
            console.error("加载乐段失败：", error);
        });
}
document.addEventListener("DOMContentLoaded", loadNoteBlocks);

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