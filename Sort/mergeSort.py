def merge(left, right):
    merged = []
    i = 0
    j = 0
    while (i < len(left) and j < len(right)):
        if (left[i] <= right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])

    return merged

def mergeSort(s):
    
    if len(s) <= 1:
        return s
    
    mid = len(s) // 2
    
    left = s[:mid]
    right = s[mid:]

    left = mergeSort(left)
    right = mergeSort(right)

    return merge(left, right)

if __name__ == "__main__":
    
    s = [3,44,38,5,47,15,36,26,27,2,46,4,19,1,50,48]
    print(mergeSort(s))
