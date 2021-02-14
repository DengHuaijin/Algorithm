class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def isSubStructure(A: TreeNode, B: TreeNode):

    def dfs(a, b):
        if not b: return True
        if not a or (a.val != b.val): return False
        return dfs(a.left, b.left) and dfs(a.right, b.right)

    return bool(a and b) and (dfs(A, B) or isSubStructure(A.left, B) or isSubStructure(A.right, B))
