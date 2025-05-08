n, m = map(int, input().split())
a = [int(x) for x in input().split()]
b = [0] * n
b[a[0]%n] = 1
lighted = 1

for i in a[1:]:
    if b[i%n] == 0 and (b[(i+1)%n] == 1 or b[i-1%n] == 1):
        b[i%n] = 1
        lighted += 1
    if lighted == n:
        print(a[0], i)
        break

if lighted < n:
    print("No")
