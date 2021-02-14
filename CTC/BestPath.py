from __future__ import absolute_import, print_function, division

from itertools import groupby
import numpy as np

def ctcBestPath(mat, chars):

    # 时间方向维度不变，chars方向保留最大值得index
    best_path = np.argmax(mat, axis = 1)
    best_chars = [chars[k] for k,_ in groupby(best_path) if k != len(chars)]
    res = "".join(best_chars)

    return res

def testBestPath():
    chars = "abc"
    mat = np.array([[0.2,0,0.6,0.2], [0.2,0,0.6,0.2], [0.2,0.3,0.1,0.4]])
    expected = "cc"
    pred = ctcBestPath(mat, chars)
    print(pred)
    print("OK" if expected == pred else "ERROR")


if __name__ == "__main__":
    testBestPath()
