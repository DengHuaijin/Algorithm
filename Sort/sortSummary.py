import time
import numpy as np
import matplotlib.pyplot as plt
from quickSort import quickSort
from bubbleSort import bubbleSort

if __name__ == "__main__":

    step = 50
    x1, y1 = [], []
    x2, y2 = [], []
    for scale in range(10, 5000+step, step):
        # print(scale, end = "\r")
        s = np.random.randint(0,50,(scale))
        
        start = time.time()
        _ = quickSort(s)
        end = time.time()
        x1.append(scale)
        y1.append(end-start)
        print(end-start)
        start = time.time()
        _ = bubbleSort(s)
        end = time.time()
        x2.append(scale)
        y2.append(end-start)

    plt.figure()
    plt.plot(x1, y1, color = "r", label = "quickSort")
    plt.plot(x2, y2, color = "g", label = "bubbleSort")
    plt.legend(loc = "upper right")

    plt.savefig("./time.png")
