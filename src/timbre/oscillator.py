import numpy as np
import matplotlib.pyplot as plt

def oscillator(wave_type: str,
               frequency: float,
               t: list) -> np.ndarray:
    """
    Generate an audio waveform of given type.

    Parameters:
    - wave_type: 'sine', 'square', 'sawtooth', or 'triangle'
    - frequency: Frequency of the waveform in Hz
    - sample_rate: Samples per second (default 44100)
    - duration: Duration of the signal in seconds

    Returns:
    - A numpy array containing the generated waveform.
    """
    if wave_type == 'sine':
        # Sine wave: sin(2πft)
        return np.sin(2 * np.pi * frequency * t)

    elif wave_type == 'square':
        # Square wave: sign of sine
        return np.sign(np.sin(2 * np.pi * frequency * t))

    elif wave_type == 'sawtooth':
        # Sawtooth wave: ramps from -1 to 1
        return 2 * (t * frequency - np.floor(0.5 + t * frequency))

    elif wave_type == 'triangle':
        # Triangle wave: absolute sawtooth
        return 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1

    else:
        raise ValueError(f"Unsupported wave_type: {wave_type}. Choose from 'sine', 'square', 'sawtooth', 'triangle'.")
    
if __name__ == '__main__':
    wave = oscillator('triangle', frequency=440, duration=0.005)
    plt.plot(wave)
    plt.title('440 Hz Sine Wave')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.show()

