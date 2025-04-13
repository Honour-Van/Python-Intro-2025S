n = int(input())
m = int(input())
while (m != 0):
    r = n % m
    n = m
    m = r
print(n)
