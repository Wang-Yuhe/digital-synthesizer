// ================= 左侧轨道面板 =================
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