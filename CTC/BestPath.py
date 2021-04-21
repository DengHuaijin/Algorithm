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
    mat_word = softmax(loadNNOutput("data/rnnOutput_word.csv"))
    mat_sentence = softmax(loadNNOutput("data/rnnOutput_sentence.csv"))
    print("All tokens: {}".format(len(chars)))
    print("word rnn output: {}".format(mat_word.shape))
    print("sentence rnn output: {}".format(mat_sentence.shape))
    print("word best path: ", ctcBestPath(mat_word, chars))
    print("sentence best path: ", ctcBestPath(mat_sentence, chars))

if __name__ == "__main__":
    testBestPath()
