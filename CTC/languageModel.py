import codecs
import re

class languageModel:
    def __init__(self, data, chars):
        self.initWordList(data)
        self.initCharBigram(data, chars)

    def initWordList(self, data):
        txt = open(data).read().lower()
        words = re.findall(r'\w+', txt)
        self.words = list(filter(lambda x:x.isalpha(), words))

    def initCharBigram(self, data, chars):
        """
        {a: {a:0, b:0, c:0, ..., z:0}, 
         b: {a:0, b:0, c:0, ..., z:0}, 
         ...}
         统计aa ab ac ad..的数量
        """
        self.bigram = {c: {d: 0 for d in chars} for c in chars}

        txt = codecs.open(data, 'r', 'utf-8').read()
        for i in range(len(txt)-1):
            pre = txt[i]
            cur = txt[i+1]

            if pre not in self.bigram or cur not in self.bigram[pre]:
                continue

            self.bigram[pre][cur] += 1

    def getCharBigram(self, pre, cur):
        pre = pre if pre else " "
        cur = cur if cur else " "

        numBigrams = sum(self.bigram[pre].values())
        if numBigrams == 0:
            return 0
        return self.bigram[pre][cur] / numBigrams

    def getWordList(self):
        return self.words
