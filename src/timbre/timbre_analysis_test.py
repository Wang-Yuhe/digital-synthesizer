import numpy as np
import librosa
import scipy.signal

def timbre_analysis_dict(
    filename: str,
    frame_length: int = 2048,#窗口大小
    hop_length: int = 512,#移动步长
    n_harmonics: int = 10,
    fmin: float = 50,
    fmax: float = 3000
) -> dict[float, list[float]]:
    """
    对旋律或多音（单音/多音）音频：
      1) 降噪
      2) 逐帧基频跟踪（YIN）
      3) 提取每个基频的前 n_harmonics 谐波幅度并归一化
    返回：
      一个 dict，key = f0（Hz），value = [h1_rel, h2_rel, …, hN_rel]
    """
    y, sr = librosa.load(filename, sr=None)

    # 基频跟踪
    f0_series, voiced_flag, voiced_prob = librosa.pyin(y, fmin=fmin, fmax=fmax, 
                    sr=sr,frame_length=frame_length, hop_length=hop_length)#pyin效果更好
    
    S = np.abs(librosa.stft(y, n_fft=frame_length, hop_length=hop_length))#短时傅里叶变换
    #S[f, t]第t帧频率f上的振幅
    freqs = np.linspace(0, sr/2, num=S.shape[0])

    # 遍历每帧，构建 {f0: [harmonics…]} 字典
    result = []
    result_notename = []
    for t, f0 in enumerate(f0_series):
        if np.isnan(f0) or f0 <= 0 or not voiced_flag[t] or voiced_prob[t]<0.3:
            continue
        mags = []
        for h in range(1, n_harmonics + 1):
            #原来的谐波成分是找频率点，而事实上有时并不完全为整数倍，这里找范围内峰值最高的
            target_freq = f0 * h
            search_radius = 30
            mask = np.where((freqs >= target_freq - search_radius) & (freqs <= target_freq + search_radius))[0]
            
            if len(mask) == 0:
                mags.append(0.0)
                continue

            local_mags = S[mask, t]
            max_idx_in_window = np.argmax(local_mags)
            mags.append(local_mags[max_idx_in_window])

        mags = np.array(mags)
        rel = (mags / (mags[0] + 1e-8)).tolist()
        result_notename.append(librosa.midi_to_note(librosa.hz_to_midi(f0), octave=True))
        result.append(rel)
    
    grouped_names = []
    grouped_results = []
    current_name = result_notename[0]
    buffer = [result[0]]
    for name, vec in zip(result_notename[1:], result[1:]):
        if name == current_name:
            buffer.append(vec)
        else:
            avg_vec = np.mean(buffer, axis=0).tolist()
            grouped_names.append(current_name)
            grouped_results.append(avg_vec)
            current_name = name
            buffer = [vec]
    avg_vec = np.mean(buffer, axis=0).tolist()
    grouped_names.append(current_name)
    grouped_results.append(avg_vec)

    return grouped_names, grouped_results

if __name__ == "__main__":
    filename = "E:/test.wav"
    notename, result = timbre_analysis_dict(filename)
    print(notename)
    """
    for i in range(len(result)):
        print(f"pitch:{notename[i]}")
        print(result[i])
        print()
    """
