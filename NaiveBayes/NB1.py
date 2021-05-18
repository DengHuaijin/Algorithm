"""
编写Naïve Bayes分类模型对邮件文本进行分类，判断该邮件是不是垃圾邮件（二分类）。我们已经通过数据预处理，将原始的邮件文本数据转化为分类器可用的数据向量形式，具体：数据表示为整型数向量x=(x1,x2,…,xd)。d是数据特征向量的维数，每个输入数据样本的格式为:
Label x1 x2 ... xd
其中Label为0或者1的整型数字（0表示正常邮件，1表示垃圾邮件）；

        x1 x2 ... xd是离散化后的特征，表示为从0开始的自然数；

        维度d小于20；

        如果Label=?，则表示希望输出的预测类别值（需要预测的类别一定已在对应的训练数据中已经出现过）。
输入格式如下：
第一行三个数字M N d，M是训练集的大小，N是测试集的大小，d是数据维数。接下来是M行训练数据样本,然后是N行需要预测的样本。
4   2   3
1   13  0   10
0   6   11  2
1   17  2   14
0   8   16  13
?   20  3   19
?   2   13  18

1
0
"""
import math
line = list(map(int, input().rstrip().split()))
M, N, d = line[0], line[1], line[2]
train_data = {}
test_data = []
train_data[0] = []
train_data[1] = []
for _ in range(M):
    line = list(map(int, input().rstrip().split()))
    train_data[line[0]].append(line[1:])
for _ in range(N):
    test_data.append(list(map(int, input().rstrip().split()[1:])))

def trainNB(train_data):
    train_size = M
    size0 = len(train_data[0])
    size1 = len(train_data[1])
    featureCount0 = [1] * d
    featureCount1 = [1] * d
    total0 = 2.0
    total1 = 2.0
    for i in range(size0):
        for j in range(d):
            featureCount0[j] += train_data[0][i][j]
        total0 += sum(train_data[0][i])
    for i in range(size1):
        for j in range(d):
            featureCount1[j] += train_data[1][i][j]
        total1 += sum(train_data[1][i])
    feature0 = [math.log(i / total0) for i in featureCount0]
    feature1 = [math.log(i / total1) for i in featureCount1]
    return feature0, feature1, size0 / train_size, size1 / train_size

def classifyNB(data, feature0, feature1, pclass0, pclass1):
    p0 = 0
    p1 = 0
    for i in range(len(data)):
        p0 += data[i] * feature0[i]
        p1 += data[i] * feature1[i]
    p0 += math.log(pclass0)
    p1 += math.log(pclass1)
    if p0 >= p1:
        return 0
    else:
        return 1
feature0, feature1, pclass0, pclass1 = trainNB(train_data)
for data in test_data:
    print(classifyNB(data, feature0, feature1, pclass0, pclass1))
