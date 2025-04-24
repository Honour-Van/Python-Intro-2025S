n = int(input())
deps = {}
for i in range(1, n + 1):
    l = input().split()
    for j in l[1:]:
        deps[i] = deps.get(i, []) + [int(j)]

s = set()
def dfs(n):
    global s
    for i in deps.get(n, []):
        s.add(i)
        dfs(i)
    return

dfs(1)
print(len(s) + 1)