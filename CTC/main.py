from __future__ import absolute_import, print_function, division
from __future__ import literal_unicode

import BestPath
import BeamSearch
import Loss
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

def wordRecognition():

    chars = ' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    mat = softmax(loadNNOutput())

    ground_truth = "aircraft"
    print("TARGET : ", ground_truth)
    print("BEST_PATH: ", BestPath.ctcBestPath(mat, chars))
    print("BEAM SEARCH: ", BeamSearch.ctcBeamSearch(mat, chars, None))
    print("PROB: ", Loss.ctcLabelingProb(mat, ground_truth, chars))
    print("LOSS: ", Loss.ctcLoss(mat, ground_truth, chars))

if __name__ == "__main__":

    print("=====word recognition=====")
    wordRecognition()

