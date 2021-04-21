import math
import numpy as np
from Common import softmax, loadNNOutput, parser

def multiply(nums: list):
    res = 1
    for i in nums:
        res *= i
    return res

def ctcRegularBeamSearch(mat, chars, beam):
    # sequences 存储最优的beam个序列
    sequences = [[[], 0.0]]
    T, _ = mat.shape

    for t in range(T):
        all_candidates = []
        for i in range(len(sequences)):
            # 基于每条最优path进行扩展
            seq, score = sequences[i]
            for j in range(len(mat[0])):
                # 遍历当前帧每一个token
                candidate = [seq + [j], score - math.log(mat[t][j])]
                all_candidates.append(candidate)
        ordered = sorted(all_candidates, key = lambda x: x[1])
        sequences = ordered[:beam]
    return sequences

def test():
    
    chars = ' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    mat = softmax(loadNNOutput("data/rnnOutput_sentence.csv"))
    print("All tokens: {}".format(len(chars)))
    print("rnn output: {}".format(mat.shape))
    sequences = ctcRegularBeamSearch(mat, chars, 4)
    for seq in sequences:
        print(parser(seq[0], chars))

if __name__ == "__main__":
    test()
