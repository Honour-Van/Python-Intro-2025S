a = int(input())
b = int(input())

if a > b:
    a, b = b, a
ans = 0
for i in range(a, b+1):
    if i % 2:
        ans += i

print(ans)