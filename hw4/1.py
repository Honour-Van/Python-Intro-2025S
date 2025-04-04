a, b, m = map(int, input().split())

if m == 2:
    print(b)
else:
    ans = 0
    for i in range(3, m + 1):
        ans = a + 2 * b
        a, b = b, ans
    print(ans)