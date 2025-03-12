old = float(input())
ans = 0
if old <= 500:
    ans = old
elif 500 < old <= 2000:
    ans = 500 + (old - 500) * 0.9
elif 2000 < old <= 5000:
    ans = 500 + 1500 * 0.9 + (old - 2000) * 0.8
elif old > 5000:
    ans = 500 + 1500 * 0.9 + 3000 * 0.8 + (old - 5000) * 0.6

print(f'{ans:.2f}')
