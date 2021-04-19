import numpy as np

def softmax(mat):
    T, H = mat.shape
    res = np.zeros(mat.shape)
    for t in range(T):
        y = mat[t, :]
        res[t, :] = np.exp(y) / np.sum(np.exp(y))
    return res

def loadNNOutput(fn):
    return np.genfromtxt(fn, delimiter = ';')[:, : -1]

def extendByBlanks(seq, b):
    # 构造出一个Z=[y1, eps, y2, eps, y3, eps...yU, eps]
    res = [b]
    for s in seq:
        res.append(s)
        res.append(b)
    return res

def wordToLabelSeq(words, classes):
    res = [classes.index(i) for i in words]
    return res

def parser(sequence, chars):
    res = ""
    sequence = list(set(sequence))
    low = 0
    for fast in range(len(sequence)):
        if sequence[fast] != len(chars):
            sequence[low] = sequence[fast]
            low += 1
    sequence = sequence[:low]
    return "".join(list(map(lambda x:chars[x], sequence)))
