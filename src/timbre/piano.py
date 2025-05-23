import numpy as np
from timbre.timbre_synthesis import timbre_synthesis

def piano(freq, duration, sample_rate, volume):
    harmonics = [1,0.340,0.102,0.085,0.070,0.065,0.028,0.010,0.014,0.012,0.013,0.004]
    waveform=timbre_synthesis(freq, duration, sample_rate, volume, harmonics, 0.01, 0.03, 0.4, 0.8)
    return waveform