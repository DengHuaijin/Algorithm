import numpy as np
import math
import sys

from Common import softmax, loadNNOutput, extendByBlanks, wordToLabelSeq

def recLabelingProb(t, s, mat, labelingWithBlanks, blank, cache):
    
    if s < 0:
        return 0.0

    if cache[t][s] != None:
        return cache[t][s]

    if t == 0:
        if s == 0:
            res = mat[0, blank]
        elif s == 1:
            res = mat[0, labelingWithBlanks[1]]
        else:
            # t=0时刻只能走到第一个token或者第二个token 其余节点概率分数均为0
            res = 0.0
        return res

    
    # 特殊节点(eps, a, eps) or (a, eps, a) 若第s个节点为eps,则s-2节点一定为eps
    if labelingWithBlanks[s] == blank or (s > 2 and labelingWithBlanks[s-2] == labelingWithBlanks[s]): 
        res = (recLabelingProb(t-1, s, mat, labelingWithBlanks, blank, cache) + \
               recLabelingProb(t-1, s-1, mat, labelingWithBlanks, blank, cache)) * mat[t, labelingWithBlanks[s]]
    else:
    # 常规节点
        res = (recLabelingProb(t-1, s, mat, labelingWithBlanks, blank, cache) + \
               recLabelingProb(t-1, s-1, mat, labelingWithBlanks, blank, cache) + \
               recLabelingProb(t-1, s-2, mat, labelingWithBlanks, blank, cache)) * mat[t, labelingWithBlanks[s]]
    
    cache[t][s] = res
    # print("t:{} s:{}".format(t, s))
    return res

def ctcLabelingPorb(label, mat, classes):
    
    maxT,_ = mat.shape
    blank = len(classes)
    # 生成中间序列 Z = (eps, a, eps, i, eps, ..., eps, t, eps)
    labelingWithBlanks = extendByBlanks(wordToLabelSeq(label, classes), blank)
    # 直接对最后两个节点求和 
    cache = [[None]*len(labelingWithBlanks) for _ in range(maxT)]
    return recLabelingProb(maxT-1, len(labelingWithBlanks)-1, mat, labelingWithBlanks, blank, cache) + \
           recLabelingProb(maxT-1, len(labelingWithBlanks)-2, mat, labelingWithBlanks, blank, cache)

def ctcLoss(label, mat, classes):
    return -math.log(ctcLabelingPorb(label, mat, classes))

def testLoss():

    chars = ' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    mat = softmax(loadNNOutput("data/rnnOutput.csv"))
    print("rnn output shape: {} all tokens: {}".format(mat.shape, len(chars)))
    ground_truth = "aircraft"

    print("ground truth: {}\nLoss: {}".format(ground_truth, ctcLoss(ground_truth, mat, chars)))

if __name__ == "__main__":
    testLoss()
