n = int(input())

l = int(n ** 0.5)
# print(l)
cnt = 0
for i in range(1, l + 1):
    j = n // i
    if i * j == n:
        cnt += 1
print(cnt)