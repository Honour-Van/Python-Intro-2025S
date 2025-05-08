def check(num):
    s = 1
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            s += i + num // i
    return s == num

n = int(input())
flag = 0
for i in range(2, n):
    if check(i):
        print(i)
        flag = True
if not flag:
    print("No")
