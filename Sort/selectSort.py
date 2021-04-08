
def selectSort(s: list):
    l = len(s)
    if l == 1:
        return s

    for i in range(l-1):
        for j in range(i+1, l):
            if s[j] < s[i]:
                tmp = s[j]
                s[j] = s[i]
                s[i] = tmp
    return s

if __name__ == "__main__":
    
    s = [3,44,38,5,47,15,36,26,27,2,46,4,19,1,50,48]
    print(selectSort(s))
