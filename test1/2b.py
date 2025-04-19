m, n = map(int, input().split())

while True:
    if sum(map(int, list(str(m)))) == 10:
        n -= 1
    if n == 0:
        print(m)
        break
    m += 1
