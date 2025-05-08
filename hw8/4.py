n = int(input())
l = []
for i in range(n):
    name, score, num = input().split()
    l.append((name, int(score), int(num)))

for i in sorted(l, key=lambda x: (-x[1], -x[2])):
    print(i[0])
