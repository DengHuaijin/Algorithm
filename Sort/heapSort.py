import math

def heapify(s, n, i):

    left = 2 * i + 1
    right = 2 * i + 2
    largest = i
    
    if left < n and s[left] > s[largest]:
        largest = left
    if right < n and s[right] > s[largest]:
        largest = right

    if largest != i:
        s[i], s[largest] = s[largest], s[i]
        heapify(s, n, largest)

def heapSort(s):
    n = len(s)
    for i in range(n, -1, -1):
        heapify(s, n, i)
    
    for i in range(n-1, 0, -1):
        s[i], s[0] = s[0], s[i]
        heapify(s, i, 0)
    return s

if __name__ == "__main__":

    s = [3,44,38,5,47,15,36,26,27,2,46,4,19,1,50,48]
    print(heapSort(s))
