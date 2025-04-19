n = int(input())
a = int(input())
cur = 1
ans = 0
for i in range(a, a + n):
    cur *= i
    ans += cur
print(ans)