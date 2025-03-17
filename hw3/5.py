a, b = map(int, input().split())

if a > b:
    a, b = b, a

no_answer = True
for i in range(a, b + 1):
    z, x, c, v = map(int, str(i))
    if z ** 4 + x ** 4 + c ** 4 + v ** 4 == i:
        print(i)
        no_answer = False
if no_answer:
    print("No Answer")
