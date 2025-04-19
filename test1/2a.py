n = int(input())

xmax = min(n // 52, 100)
for x in range(xmax, 0, -1):
    d = 52 * (7 * x)
    for k in range(1, n):
        e = d + 52 * (21 * k)
        if e == n:
            print(x)
            print(k)
            exit()
        elif e > n:
            break
