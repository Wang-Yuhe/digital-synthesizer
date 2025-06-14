"""振荡器"""
import numpy as np
import matplotlib.pyplot as plt

def oscillator(wave_type: str, frequency: float, t: list) -> np.ndarray:
    """
    振荡器，生成指定的波形

    Args:
        wave_type (str): 'sine', 'square', 'sawtooth', or 'triangle'
        frequency (float): 波形的频率，Hz为单位
        t (list): 采样点

    Returns:
        waveform (np.ndarray): 生成的波形
    """
    if wave_type == 'sine':
        # Sine wave: sin(2πft)
        return np.sin(2 * np.pi * frequency * t)

    if wave_type == 'square':
        # Square wave: sign of sine
        return np.sign(np.sin(2 * np.pi * frequency * t))

    if wave_type == 'sawtooth':
        # Sawtooth wave: ramps from -1 to 1
        return 2 * (t * frequency - np.floor(0.5 + t * frequency))

    if wave_type == 'triangle':
        # Triangle wave: absolute sawtooth
        return 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1

    raise ValueError(f"Unsupported wave_type: {wave_type}. Choose from 'sine', 'square', 'sawtooth', 'triangle'.")

if __name__ == '__main__': # pragma: no cover
    wave = oscillator('triangle', 440, np.linspace(0, 1.0, 44100, endpoint=False))
    plt.plot(wave)
    plt.title('440 Hz Sine Wave')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.show()
