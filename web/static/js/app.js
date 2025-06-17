function loadNoteBlocks() {
    fetch('/get_note_blocks')  // 调用 Flask 的路由
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('note-block-container');
            container.innerHTML = '';  // 清空旧的内容

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

// 页面加载完就初始化一次
document.addEventListener("DOMContentLoaded", loadNoteBlocks);

function toggleFolder(element) {
    const content = element.nextElementSibling;
    if (content.style.display === "none") {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
}

// 渲染note_blocks列表的函数
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

// 添加声轨按钮事件
document.getElementById('add-track-btn').addEventListener('click', () => {
    fetch('/add_track', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            alert('添加声轨成功');
            renderNoteBlocks(data.note_blocks);
            loadNoteBlocks();
        })
        .catch(err => {
            console.error(err);
            alert('调用失败');
        });
});

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
