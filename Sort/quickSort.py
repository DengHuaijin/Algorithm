def quickSort(s):
    
    left = []
    right = []
    if len(s) < 1:
        return s

    pivot = s[0]
    pivotCount = 0

    for i in range(len(s)):
        if s[i] < pivot:
            left.append(s[i])
        elif s[i] > pivot:
            right.append(s[i])
        else:
            pivotCount += 1

    left = quickSort(left)
    right = quickSort(right)

    return left + pivotCount * [pivot] + right

if __name__ == "__main__":
    
    s = [3,44,38,5,47,15,36,26,27,2,46,4,19,1,50,48]
    print(quickSort(s))
