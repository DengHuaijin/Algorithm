def bubbleSort(s):
    change = True    
    while change:
        change = False
        for i in range(len(s) - 1):
            if s[i] > s[i+1]:
                s[i], s[i+1] = s[i+1], s[i]
                change = True
    return s

if __name__ == "__main__":
    
    s = [3,44,38,5,47,15,36,26,27,2,46,4,19,1,50,48]
    print(bubbleSort(s))
