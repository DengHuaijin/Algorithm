"""
回溯算法模板：

res = []
path = []

def backtrack(为探索区域,res,path):
    if path 满足条件:
        res.add(path) # 深度拷贝
        满足结束条件时 return
    for 选择 in 为探索区域当前可能的选择:
        if 当前选择符合要求:
            path.add(当前选择)
            backtrack(新的未探索区域,res,path)
            path.pop()
"""

import copy 

def backtrack(nums, index, res, path):
    """
    如果是全局path,这里就必须用深度拷贝
    """
    res.append(copy.deepcopy(path)) 
    if index >= len(nums):
        return
    for i in range(index, len(nums)):
        if i > index and nums[i] == nums[i-1]:
            continue
        path.append(nums[i])
        backtrack(nums, i+1, res, path)
        path.pop()

if __name__ == "__main__":
    nums = [1,2,2]
    nums = sorted(nums)
    res = []
    path = []
    backtrack(nums, 0, res, path)
    print(res)
