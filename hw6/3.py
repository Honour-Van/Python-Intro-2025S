nums = dict()
prices = dict()

n, m = map(int, input().split())

for i in range(n):
    name, price, num = input().split()
    price = int(price)
    num = int(num)
    nums[name] = num
    prices[name] = price

avn = 0
for i in range(m):
    for j in input().split():
        if nums[j]:
            nums[j] -= 1
            avn += prices[j]
print(avn)
