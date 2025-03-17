n = int(input())
ans = 0
for _ in range(n):
    ans += int(input())
print(ans)
if ans >= 60:
    print("P")
else:
    print("F")