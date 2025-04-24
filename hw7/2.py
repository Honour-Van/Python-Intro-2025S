def gcd(num1, num2):
    if num1 < num2:
        num1, num2 = num2, num1
    if num1 % num2 == 0:
        return num2
    return gcd(num2, num1 % num2)
n = int(input())
for _ in range(n):
    a, b = map(int, input().split())
    g = gcd(a, b)
    print(g, a * b // g)
