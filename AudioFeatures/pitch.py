import os,sys
import math
import librosa
import numpy as np
import scipy.io.wavfile as wave

def pitch_detection(data, sample_freq, window_length, window_stride,
                    fmin, fmax):
    
    data = data * 1.0 / (max(data) + 0.00001)
    n_window_length = window_length * sample_freq
    n_window_stride = window_stride * sample_freq
    num_fft = 2 ** math.ceil(math.log2(n_window_length))
    pitches, mag = librosa.core.piptrack(y = data, sr = sample_freq,
                          S = None, n_fft = num_fft,
                          hop_length = int(n_window_stride),
                          fmin = fmin, fmax = fmax,
                          threshold = 0.75)
    # pitchs, mag [f, T] f <= nfft
    pitch_max = [max(pitches[:, t]) for t in range(pitches.shape[1])]
    mag_max = [max(mag[:, t]) for t in range(mag.shape[1])]

    return pitch_max

if __name__ == "__main__":

    sample_freq, data = wave.read("test.wav")
    # data, sample_freq = librosa.load("test.wav", sr = 16000)
    window_length = 0.03
    window_stride = 0.01
    fmin = 80
    fmax = 250

    pitch_max = pitch_detection(data, sample_freq, window_length, window_stride, fmin, fmax)
