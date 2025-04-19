n = int(input())

d = dict()
for i in range(n):
    name = input()
    d[name] = d.get(name, []) + [i]

for k, v in sorted(d.items()):
    print(f"{k} : {' '.join(map(str, v))}")
