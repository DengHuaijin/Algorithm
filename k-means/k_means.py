import sys
import math
import numpy as np
import matplotlib.pyplot as plt

def distance(x1, x2):
    
    if len(x1) != len(x2):
        raise ValueError("the dimension of x1 and x2 must be the same")
    
    res = 0
    for i in range(len(x1)):
        res += abs(x1[i] - x2[i])**2

    return math.sqrt(res)

if __name__ == "__main__":

    f = open("data", "r")
    data = []
    for line in f.readlines():
        data.append(list(map(float, line.rstrip().split(" "))))

    k = 3
    iteration = 20
    N = len(data)
    mu = {}
    C = {}
    
    for i in range(k):
        mu[i] = data[np.random.randint(N)]
        C[i] = []
    
    for it in range(iteration):
        for i in range(k):
            C[i] = []
        for i in range(N):
            tmp = []
            for j in range(k):
                tmp.append(distance(data[i], mu[j]))
            cindex = np.argmin(tmp)
            C[cindex].append(data[i])

        for i in range(k):
            mu[i] = np.mean(C[i], axis = 0)
    
        print("iter {}: {}".format(it, mu))
    
    print(N, len(C[0]) + len(C[1]) + len(C[2]))
    color = ["r", "g", "b"]
    plt.figure()
    for i in range(k):
        x = [C[i][j][0] for j in range(len(C[i]))]
        y = [C[i][j][1] for j in range(len(C[i]))]
        plt.scatter(x, y, color = color[i])

    plt.savefig("./figure.png")
