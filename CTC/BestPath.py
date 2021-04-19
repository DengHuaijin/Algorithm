from __future__ import absolute_import, print_function, division

from itertools import groupby
from Common import softmax, loadNNOutput, parser
import numpy as np


def ctcBestPath(mat, chars):

    # 时间方向维度不变，chars方向保留最大值得index
    best_path = np.argmax(mat, axis = 1)
    # best_chars = [chars[k] for k,_ in groupby(best_path) if k != len(chars)]
    best_chars = parser(best_path, chars)
    res = "".join(best_chars)

    return res

def testBestPath():

    chars = ' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    mat = softmax(loadNNOutput("data/rnnOutput_word.csv"))
    print("All tokens: {}".format(len(chars)))
    print("rnn output: {}".format(mat.shape))
    print(ctcBestPath(mat, chars))

if __name__ == "__main__":
    testBestPath()
