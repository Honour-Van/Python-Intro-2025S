n = int(input())
mat = []
for i in range(n):
    mat.append(list(map(int, input().split())))

def dfs(i, j):
    if i >= n or j >= n:
        return False
    if mat[i][j] == 1:
        return False
    if i == n - 1 and j == n - 1:
        return True
    if dfs(i + 1, j):
        return True
    if dfs(i, j + 1):
        return True


if dfs(0, 0):
    print("Yes")
else:
    print("No")
