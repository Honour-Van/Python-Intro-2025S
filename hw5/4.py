grade = []
n = int(input())
for i in range(n):
    grade.append([float(g) for g in input().split(" ")])

for g in grade:
    print(f'{sum(g):.1f} {sum(g) / 3:.1f}')
