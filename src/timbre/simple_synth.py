"""基于钢琴音色的自定义音色合成"""
import numpy as np
from timbre.adsr import apply_adsr
from timbre.filter import lowpass_filter, band_filter
from timbre.oscillator import oscillator

def simple_synth(
    freq: float,
    duration: float,
    sample_rate: int = 44100,
    volume: float = 1.0,
    harmonics: list = None,
    detune: float = 0.0,
    inharmonicity: float = 0.0,
    lfo_rate: float = 0.0,
    lfo_depth: float = 0.0,
    adsr_params: tuple = (0.01, 0.1, 0.8, 0.2),
    filter_type: str = 'lowpass',
    filter_cutoff: float = 5000,
    filter_order: int = 4,
    noise_level: float = 0.0
) -> np.ndarray:
    """
    A simple customizable synthesizer based on a piano timbre template.

    Parameters:
    - freq: Fundamental frequency in Hz.
    - duration: Note duration in seconds.
    - sample_rate: Sampling rate (default 44100).
    - volume: Output amplitude scaling (0.0 to 1.0).
    - harmonics: Amplitude list for each harmonic (list of floats). If None, defaults to first 8 harmonics.
    - detune: Proportion of random detune applied to each harmonic.
    - inharmonicity: Inharmonicity coefficient B applied to harmonic frequencies.
    - lfo_rate: Low-frequency oscillator rate in Hz for vibrato.
    - lfo_depth: Depth of vibrato in Hz.
    - adsr_params: ADSR envelope parameters (attack, decay, sustain_level, release).
    - filter_type: 'lowpass' or 'bandpass'.
    - filter_cutoff: Cutoff frequency for lowpass or center frequency for bandpass.
    - filter_order: Filter order.
    - noise_level: Amplitude of added white noise (0.0 to 1.0).

    Returns:
    - Numpy array containing the synthesized waveform.
    """
    # Default harmonics if not provided
    if harmonics is None:
        harmonics = [1.0] + [0.5 / (i+1) for i in range(1, 8)]

    # Time vector
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    waveform = np.zeros_like(t)

    # Build harmonic series
    for i, amp in enumerate(harmonics):
        # Calculate inharmonic frequency
        h_freq = freq * (i+1) * np.sqrt(1 + inharmonicity * (i+1)**2)
        # Apply detune
        if detune > 0.0:
            h_freq *= (1 + (np.random.rand() - 0.5) * detune)
        # Apply LFO vibrato
        if lfo_rate > 0.0 and lfo_depth > 0.0:
            lfo = np.sin(2 * np.pi * lfo_rate * t)
            h_freq = h_freq + lfo_depth * lfo
        # Generate waveform
        waveform += amp * oscillator('sine', h_freq, t)

    # Add white noise
    if noise_level > 0.0:
        noise = np.random.randn(len(t)) * noise_level
        waveform += noise

    # Normalize before envelope
    waveform /= np.max(np.abs(waveform) + 1e-12)

    # Apply ADSR envelope
    attack, decay, sustain, release = adsr_params
    waveform = apply_adsr(waveform, sample_rate, attack, decay, sustain, release)

    # Apply filter
    if filter_type == 'lowpass':
        waveform = lowpass_filter(waveform, filter_cutoff, filter_order, sample_rate)
    elif filter_type == 'bandpass':
        waveform = band_filter(waveform, filter_cutoff, filter_order, sample_rate)

    # Final volume scaling
    waveform *= volume

    # Normalize output
    waveform /= np.max(np.abs(waveform) + 1e-12)
    waveform *= volume

    return waveform


if __name__ == '__main__':
    # Example: 440 Hz note with vibrato and noise
    import matplotlib.pyplot as plt
    wave = simple_synth(
        freq=440,
        duration=0.5,
        volume=0.8,
        lfo_rate=5.0,
        lfo_depth=2.0,
        noise_level=0.02
    )
    plt.plot(wave[:1000])
    plt.title('Custom Synth 440 Hz Note')
    plt.show()
