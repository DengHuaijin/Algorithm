import numpy as np
from Common import softmax, loadNNOutput

def multiply(nums: list):
    res = 1
    for i in nums:
        res *= i
    return res

def ctcRegularBeamSearch(mat, chars):
    BW = 4
    beams = []
    bestBeams = [[] * BW]
    T, _ = mat.shape()

    for t in range(T):
        beams = sorted(beams, key = lambda x: multiply(x))
        for i in range(BW):
            bestBeams[i] = beams[i]
        beams = []
        for b in bestBeams:


def test():
    
    chars = ' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    mat = softmax(loadNNOutput("data/rnnOutput_word.csv"))
    print("All tokens: {}".format(len(chars)))
    print("rnn output: {}".format(mat.shape))
    ctcRegularBeamSearch(mat, chars)

if __name__ == "__main__":
    test()
