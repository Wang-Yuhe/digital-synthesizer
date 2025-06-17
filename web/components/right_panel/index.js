function loadNoteBlocks() {
    fetch('/left_panel/get_note_blocks')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('note-block-container');
            container.innerHTML = '';
            if (data.note_blocks.length === 0) {
                container.innerHTML = `<div class="empty-segment-placeholder">
                    在这里添加循环乐段或双击创建片段
                </div>`;
                return;
            }
            data.note_blocks.forEach(block => {
                const div = document.createElement('div');
                div.className = 'note-block-item p-2 rounded';
                div.style.backgroundColor = '#333';
                div.style.cursor = 'pointer';
                div.textContent = `乐段 #${block.index} - 音色: ${block.timbre}`;
                container.appendChild(div);
            });
        })
        .catch(error => console.error("加载乐段失败：", error));
}

document.addEventListener("DOMContentLoaded", loadNoteBlocks);

document.getElementById('add-track-btn').addEventListener('click', () => {
    fetch('/left_panel/add_track', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            alert('添加声轨成功');
            loadNoteBlocks();
        })
        .catch(err => {
            console.error(err);
            alert('调用失败');
        });
});

document.getElementById('play-btn')?.addEventListener('click', () => {
    fetch('/left_panel/play', { method: 'POST' })
        .then(res => res.json())
        .then(data => alert(data.message))
        .catch(() => alert('播放失败'));
});
