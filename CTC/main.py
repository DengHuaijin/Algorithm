from __future__ import absolute_import, print_function, division

import BestPath
import BeamSearch
import Loss
import numpy as np
from Common import softmax, loadNNOutput

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

