n = int(input())

a, b = n // 2, 1
for i in range(0, n//2):
    print(a * 'O' + b * 'X' + a * 'O')
    a -= 1
    b += 2
for i in range(n // 2, n):
    print(a * 'O' + b * 'X' + a * 'O')
    a += 1
    b -= 2
