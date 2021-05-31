import numpy as np
import scipy.io.wavfile as wave
from scipy.fftpack.realtransforms import dct

def hz2mel(freq):
    # m = m0 * log(f/f0+1)
    return 2595 * np.log(freq / 700.0 + 1.0)

def mel2hz(m):
    return 700 * (np.exp(m / 2595) - 1.0)

# 生成mel谱的filter bank
# 由若干三角形带通滤波器组成
def melFilterBank(fs, N, numChannels):
    fmax = fs / 2
    melmax = hz2mel(fmax)

    nmax = N // 2
    # 频率精度
    df = fs / N
    dmel = melmax / (numChannels + 1)
    # mel尺度下各个带通滤波器的中心频率
    melcenters = range(1, numChannels+1) * dmel

    fcenters = mel2hz(melcenters)
    # 每个滤波器中心频率对应的下标
    indexcenter = np.round(fcenters / df)
    # 每个滤波器起始频率对应的下标
    indexstart = np.hstack(([0], indexcenter[0:numChannels-1]))
    indexend = np.hstack((indexcenter[1:numChannels], [nmax]))
    filterbank = np.zeros(shape = [numChannels, nmax])

    for c in range(numChannels):
        # 三角形上升部分
        increment = 1.0 / (indexcenter[c] - indexstart[c])
        for i in range(int(indexstart[c]), int(indexcenter[c])):
            filterbank[c, i] = (i - indexstart[c]) * increment
        # 三角形下降部分
        decrement = 1.0 / (indexend[c] - indexcenter[c])
        for i in range(int(indexcenter[c]), int(indexcenter[c])):
            filterbank[c, i] = 1.0 - ((i - indexcenter[c]) * decrement)
    
    return filterbank, fcenters

if __name__ == "__main__":
    
    sample_freq, data = wave.read("../test.wav")
    window_length = 0.03
    window_stride = 0.01

    # 只取第一帧窗长
    x = data[:int(window_length * sample_freq)]
    hamming = np.hamming(len(x))
    x = x * hamming

    N = 1024
    spec = np.abs(np.fft.fft(x, N))[:N//2]

    filterbank, fcenters = melFilterBank(sample_freq, N, 20)
    # [1,N] * [N,C] -> [1,C]
    melspec = np.dot(spec, filterbank.T)
    ceps = dct(10 * np.log10(melspec), type = 2, norm = "ortho", axis = -1)
    nceps = 12
    mfcc = ceps[:nceps]
    print(mfcc)

