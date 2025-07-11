
# 数字音乐合成器（digital-synthesizer）

一个支持多乐器音色模拟、乐段编辑与实时播放的数字音乐合成系统，适用于音乐创作与教学场景。

---

## 核心功能

### 1. 音乐创作交互

- **乐段编辑**：通过钢琴卷帘界面（Piano Roll）可视化编辑音符，支持音符拖拽、长度调整、右键删除等操作（参考 `web/static/center_workspace/index.js` 中 `renderPianoRoll` 函数）。
- **多小节管理**：通过滑块调整总小节数（`bar-count-range` 控件），动态渲染时间轴（`renderTimeline` 函数）。
- **播放控制**：支持乐段播放、暂停、停止及播放进度跳转（`startModalPlayback`/`pauseModalPlayback`/`stopModalPlayback` 函数）。

### 2. 多乐器音色模拟

- 内置多种乐器音色模型（如大提琴 `cello.py`、短笛 `piccolo.py`、中提琴 `viola.py`），通过 ADSR 包络控制振幅变化（`src/timbre/adsr.py`）。
- 支持自定义 BPM（每分钟节拍数），适配不同演奏速度（`modal-bpm-input` 输入框）。

### 3. 后端数据管理

- 乐段数据持久化：通过 `/get_note_blocks` 和 `/save_note_block` 接口实现乐段的加载与保存（`loadNoteBlocks`/`saveNoteBlock` 函数）。
- 多轨混合支持：通过 `Track` 类管理多乐段合成（`src/track.py`）。

---


## 快速开始

### 1. 环境准备

```bash
# 安装依赖（建议使用虚拟环境）
pip install -r requirements.txt
```


### 2. 启动服务

```bash
python -m web.web  # 默认访问 http://localhost:5000
```

### 3. 使用流程

1. 通过滑块调整总小节数（默认9小节）。
2. 点击添加声轨后选择声轨便弹出可编辑的钢琴卷帘界面
3. 在钢琴卷帘界面拖拽创建/调整音符（左键添加，右键删除，长按添加不同时值的音符）。
4. 输入 BPM（默认120）后点击播放按钮试听。
5. 点击保存按钮持久化当前乐段（存储至后端）。
6. 可以在时间轴可以选择从何处开始

---

## 测试与质量

* **单元测试** ：覆盖音符解析（`Note.note_midi()`）、包络控制（`apply_adsr`）等核心功能（`tests/test_note.py`）。
* **集成测试** ：验证多乐段混合与音频输出（计划中，参考 `docs/软件测试与质量保证报告.md`）。
* **持续集成** ：通过 GitHub Actions 实现提交自动测试（配置示例见 `docs/软件工程化自动化.md`）。

---

## 扩展与贡献

* 新增乐器模型：在 `src/timbre/` 目录下添加新音色实现（需继承 ADSR 包络）。
* 优化前端交互：扩展钢琴卷帘的复制/粘贴功能（当前仅支持拖拽调整）。
* 文档完善：补充用户手册与开发指南（文档模板见 `docs/` 目录）。

---

 **项目文档** ：详细设计、测试报告与运维说明见 `docs/` 目录。
