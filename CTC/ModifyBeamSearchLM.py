from __future__ import absolute_import, print_function, division

import numpy as np
import languageModel
from Common import loadNNOutput, softmax, parser

class BeamEntry:
    def __init__(self):
        self.probTotal = 0
        self.probNonBlank = 0
        self.probBlank = 0
        # 加入语言分数
        self.probLM = 1
        self.flagLM = False
        self.labeling = ()

class BeamState:
    def __init__(self):
        """
        BeamState的entries以字典的形式存储每一条路径的
        字典的key是labeling序列，item是BeamEntry()
        """
        self.entries = {}
        
    def norm(self):
        """
        对语言分数做归一化
        """
        for (k, _) in self.entries.items():
            length = len(self.entries[k].labeling)
            self.entries[k].probLM = self.entries[k].probLM ** (1.0 / (length if length else 0.0))

    def sort(self):
        beams = [v for (_, v) in self.entries.items()]
        """
        对所有BeamEntry按照probTotal进行排序
        最后只返回labeling
        """
        sortedBeams = sorted(beams, reverse = True, key = lambda x: x.probTotal * x.probLM)
        return [x.labeling for x in sortedBeams]

def applyLM(prebeam, curbeam, chars, lm):
    if lm and not curbeam.flagLM:
        c1 = chars[prebeam.labeling[-1] if prebeam.labeling else chars.index(" ")]
        c2 = chars[curbeam.labeling[-1]]
        factor = 0.01
        bigramProb = lm.getCharBigram(c1, c2) ** factor
        curbeam.probLM = prebeam.probLM * bigramProb
        curbeam.flagLM = True

def addBeam(beamState, labeling):
    if labeling not in beamState.entries:
        beamState.entries[labeling] = BeamEntry()

def ctcBeamSearch(mat, chars, lm, beamWidth = 25):
    
    T, H = mat.shape
    blankIdx = len(chars)
    
    """
    BeamState中存储所有路径
    每一条路径对应一个BeamEntry
    probNonBlank初始化为0
    probBlank初始化为1
    """
    last = BeamState()
    labeling = ()
    last.entries[labeling] = BeamEntry()
    last.entries[labeling].probBlank = 1
    last.entries[labeling].probTotal = 1

    for t in range(T):
        curr = BeamState()
        
        bestLabelings = last.sort()[0:beamWidth]
        for labeling in bestLabelings:
            probNonBlank = 0
            """
            这里的labeling到t-1时刻位置，所以这里计算的是
            当前时刻的token和上一个token一致时的概率, 上一个token一定不能是空字符

            """
            if labeling:
                probNonBlank = last.entries[labeling].probNonBlank * mat[t, labeling[-1]]
            """
            这里计算的是以空字符结尾时的路径概率，上一个token可以是空字符，也可以不是
            blankIdx对应mat每一行最后一个概率
            """
            probBlank = last.entries[labeling].probTotal * mat[t, blankIdx]

            """
            先用上一时刻的beam个最优序列填充当前的BeamState
            初始化之后的
            probNonBlank, probBlank, probTotal = 0

            """
            addBeam(curr, labeling)
            
            curr.entries[labeling].labeling = labeling
            curr.entries[labeling].probNonBlank += probNonBlank
            curr.entries[labeling].probBlank += probBlank
            curr.entries[labeling].probTotal = probNonBlank + probBlank
            # 相同的label序列 LM分数也相同
            curr.entries[labeling].probLM = last.entries[labeling].probLM
            curr.entries[labeling].flagLM = True
            
            # 遍历当前帧所有token，对其中一条序列进行扩展 
            for c in range(H-1):
                newLabeling = labeling + (c,)

                if labeling and labeling[-1] == c:
                    probNonBlank = mat[t,c] * last.entries[labeling].probBlank
                else:
                    probNonBlank = mat[t,c] * last.entries[labeling].probTotal

                addBeam(curr, newLabeling)

                curr.entries[newLabeling].labeling = newLabeling
                curr.entries[newLabeling].probNonBlank += probNonBlank
                curr.entries[newLabeling].probTotal += probNonBlank

                applyLM(curr.entries[labeling], curr.entries[newLabeling], chars, lm)

        last = curr
    
    last.norm()
    bestLabeling = last.sort()[0]
    return "".join(list(map(lambda x:chars[x], bestLabeling)))

def testBeamSearch():

    chars = ' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    mat = softmax(loadNNOutput("data/rnnOutput_sentence.csv"))
    label_word = "aircraft"
    label_sentence = "the fake friend of the family, like the"
    lm = languageModel.languageModel("data/corpus.txt", chars)
    print("BEAM SEARCH with LM: ", ctcBeamSearch(mat, chars, lm))

if __name__ == "__main__":
    testBeamSearch()
