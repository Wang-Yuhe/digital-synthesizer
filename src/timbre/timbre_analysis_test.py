import numpy as np
import librosa
import scipy.signal
from pathlib import Path

def timbre_analysis_list(
    filename: str,
    frame_length: int = 2048,#窗口大小
    hop_length: int = 512,#移动步长
    n_harmonics: int = 16,
    fmin: float = 50,
    fmax: float = 3000
) -> tuple[list[str], list[list[float]]]:
    """
    对旋律或多音（单音/多音）音频：
      1) 逐帧基频跟踪(YIN)
      2) 提取每个基频的前 n_harmonics 谐波幅度并归一化
    return:
      两个list,对应音名和谐波成分
    """
    y, sr = librosa.load(filename, sr=None)

    # 基频跟踪
    f0_series, voiced_flag, voiced_prob = librosa.pyin(y, fmin=fmin, fmax=fmax, 
                    sr=sr,frame_length=frame_length, hop_length=hop_length)#pyin效果更好
    S = np.abs(librosa.stft(y, n_fft=frame_length, hop_length=hop_length))#短时傅里叶变换
    #S[f, t]第t帧频率f上的振幅
    freqs = np.linspace(0, sr/2, num=S.shape[0])

    result = []
    result_notename = []
    for t, f0 in enumerate(f0_series):
        if np.isnan(f0) or f0 <= 0 or not voiced_flag[t] or voiced_prob[t]<0.3:
            continue
        mags = []
        for h in range(1, n_harmonics + 1):
            #原来的谐波成分是找频率点，而事实上有时并不完全为整数倍，这里找范围内峰值最高的
            target_freq = f0 * h
            search_radius = 0.05 * target_freq 
            mask = np.where((freqs >= target_freq - search_radius) & (freqs <= target_freq + search_radius))[0]
            
            if len(mask) == 0:
                mags.append(0.0)
                continue

            local_mags = S[mask, t]
            max_idx_in_window = np.argmax(local_mags)
            mags.append(local_mags[max_idx_in_window])

        mags = np.array(mags)
        rel = (mags / mags[0]).tolist()
        result_notename.append(librosa.midi_to_note(librosa.hz_to_midi(f0)))
        result.append(rel)
    
    grouped_names = []
    grouped_results = []
    if len(result_notename)==0:return [],[]
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
    base = Path(__file__).resolve().parent.parent
    filename = base.parent / 'audio' / 'piano' / 'test.wav'
    notename, result = timbre_analysis_list(filename)
    #print(notename)
    #"""
    for i in range(len(result)):
        print(f"pitch:{notename[i]}")
        print(result[i])
        print()
    #"""
