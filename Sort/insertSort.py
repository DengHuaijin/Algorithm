
def insertSort(s: list):
    # 0-0位置上有序 0-1位置上有序 0-2位置上有序...
    if len(s) == 1:
        return s

    l = len(s)
    for i in range(l):
        for j in range(i,0,-1):
            if i == 0:
                continue
            if s[j] < s[j-1]:
                tmp = s[j-1]
                s[j-1] = s[j]
                s[j] = tmp
    
    return s

if __name__ == "__main__":
    
    s = [3,44,38,5,47,15,36,26,27,2,46,4,19,1,50,48]
    print(insertSort(s))
