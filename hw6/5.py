n = int(input())
d = dict()
m = 0
for i in range(1, n + 1):
    for j in set(map(int, input().split(','))):
        d[j] = d.get(j, []) + [str(i)]
        m = max(m, j)
print(m)
print(','.join(d[m]))
