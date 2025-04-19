words = input().split()
d = dict()
for word in words:
    d[word] = d.get(word, 0) + 1

for k, v in sorted(d.items()):
    print(k, v)
