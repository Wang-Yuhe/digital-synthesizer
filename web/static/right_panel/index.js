// ================= 右侧素材库面板 =================
// 素材库文件夹展开/收起
function toggleFolder(element) {
    const content = element.nextElementSibling;
    if (content.style.display === "none") {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
}