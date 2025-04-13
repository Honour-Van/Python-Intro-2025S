h = int(input())
m = int(input())

total_minutes = h * 60 + m
charges = total_minutes // 23
if total_minutes % 23 != 0:
    charges += 1
print(charges * 5)
