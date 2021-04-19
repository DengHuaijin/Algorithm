from __future__ import absolute_import, print_function, division

import numpy as np
import BestPath
from Common import loadNNOutput, softmax

class BeamEntry:
    def __init__(self):
        self.probTotal = 0
        self.probNonBlank = 0
        self.probBlank = 0
        self.labeling = ()

class BeamState:
    def __init__(self):
        """
        BeamState的entries以字典的形式存储每一条路径的
        """
        self.entries = {}

    def sort(self):
        beams = [v for (_, v) in self.entries.items()]
        """
        对所有BeamEntry按照probTotal进行排序
        最后只返回labeling
        """
        sortedBeams = sorted(beams, reverse = True, key = lambda x: x.probTotal)
        return [x.labeling for x in sortedBeams]

def addBeam(beamState, labeling):
    if labeling not in beamState.entries:
        beamState.entries[labeling] = BeamEntry()

def ctcBeamSearch(mat, chars, lm, beamWidth = 25):
    
    T, H = mat.shape
    blankIdx = len(chars)
    
    """
    BeamState中存储所有路径
    每一条路径对应一个BeamEntry
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
            考虑非空的beam
            这里的labeling到t-1时刻位置，所以这里计算的是最后一个字符重复时的路径概率
            """
            if labeling:
                probNonBlank = last.entries[labeling].probNonBlank * mat[t, labeling[-1]]
            """
            这里计算的是以空字符结尾时的路径概率
            blankIdx对应mat每一行最后一个概率
            """
            probBlank = last.entries[labeling].probTotal * mat[t, blankIdx]

            addBeam(curr, labeling)

            curr.entries[labeling].labeling = labeling
            curr.entries[labeling].probNonBlank += probNonBlank
            curr.entries[labeling].probBlank += probBlank
            curr.entries[labeling].probTotal = probNonBlank + probBlank

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

        last = curr

    bestLabeling = last.sort()[0]
    bestChars = ""
    print(bestLabelings)
    
    for i in bestLabelings[0]:
        bestChars += chars[i]

    return bestChars

def testBeamSearch():

    chars = ' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    mat = softmax(loadNNOutput("data/rnnOutput.csv"))

    ground_truth = "aircraft"
    print("TARGET : ", ground_truth)
    print("BEST_PATH: ", BestPath.ctcBestPath(mat, chars))
    print("BEAM SEARCH: ", ctcBeamSearch(mat, chars, None))

if __name__ == "__main__":
    testBeamSearch()
