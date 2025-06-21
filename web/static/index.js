/*
document.getElementById('add-track-btn').addEventListener('click', () => {
    fetch('/add_track', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            alert('添加声轨成功');
            // 这里可以调用外部的渲染函数，或者触发事件让中心区更新
            // 例如: window.dispatchEvent(new Event('trackAdded'));
        })
        .catch(err => {
            console.error(err);
            alert('调用失败');
        });
});
*/