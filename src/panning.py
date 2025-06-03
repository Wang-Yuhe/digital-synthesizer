import numpy as np

def panning(waveform: np.ndarray, pan: float) -> np.ndarray:
    """
    对单声道或立体声音频进行声像移动处理。

    Args:
        waveform (np.ndarray): 音频波形数据，形状为 (n,) 或 (n, 1) 为单声道，(n, 2) 为立体声
        pan (float): 声像值，范围为 -1.0（左）到 +1.0（右）

    Returns:
        np.ndarray: 处理后的立体声波形，形状为 (n, 2)
    """
    # 保证 pan 在合法范围内
    pan = np.clip(pan, -1.0, 1.0)

    # 如果是单声道，确保形状为 (n,)
    if waveform.ndim == 2 and waveform.shape[1] == 1:
        waveform = waveform[:, 0]
    elif waveform.ndim == 1:
        pass
    elif waveform.ndim == 2 and waveform.shape[1] == 2:
        # 如果是立体声，先合成为单声道（平均），再进行 pan 操作
        waveform = waveform.mean(axis=1)
    else:
        raise ValueError("Unsupported waveform shape")

    # 计算左右声道增益
    left_gain = (1.0 - pan) / 2.0
    right_gain = (1.0 + pan) / 2.0

    # 应用增益
    left = waveform * left_gain
    right = waveform * right_gain

    # 合并成立体声 (n, 2)
    stereo_waveform = np.stack([left, right], axis=1)

    return stereo_waveform


def dynamic_panning(waveform: np.ndarray, start_pan: float = -1.0, end_pan: float = 1.0, chunk_size: int = 1024) -> np.ndarray:
    """
    对音频波形进行动态声像移动，从 start_pan 平滑过渡到 end_pan。
    
    Args:
        waveform (np.ndarray): 输入音频，单声道 shape=(n,) 或立体声 shape=(n, 2)
        start_pan (float): 起始声像位置（-1 左，0 中，+1 右）
        end_pan (float): 结束声像位置
        chunk_size (int): 每个处理块的样本数（越小越平滑）

    Returns:
        np.ndarray: 处理后的立体声音频，shape=(n_samples, 2)
    """
    # 预处理成单声道
    if waveform.ndim == 2:
        if waveform.shape[1] == 2:
            waveform = waveform.mean(axis=1)
        elif waveform.shape[1] == 1:
            waveform = waveform[:, 0]
        else:
            raise ValueError("Unsupported number of channels")
    
    num_samples = waveform.shape[0]
    num_chunks = int(np.ceil(num_samples / chunk_size))

    # 生成平滑过渡的 pan 值序列
    pan_values = np.linspace(start_pan, end_pan, num_chunks)

    # 创建输出立体声数组
    stereo_output = np.zeros((num_samples, 2), dtype=np.float32)

    for i in range(num_chunks):
        start = i * chunk_size
        end = min(start + chunk_size, num_samples)
        chunk = waveform[start:end]
        
        pan = pan_values[i]
        left_gain = (1.0 - pan) / 2.0
        right_gain = (1.0 + pan) / 2.0

        stereo_output[start:end, 0] = chunk * left_gain  # 左声道
        stereo_output[start:end, 1] = chunk * right_gain  # 右声道

    return stereo_output

