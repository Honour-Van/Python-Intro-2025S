speed = int(input())
ride = int(input())
water = int(input())

cnt = 0
if speed > 15:
    cnt += 1
if ride > 30:
    cnt += 1
if 0 <= water <= 5:
    cnt += 1
if water == -1:
    cnt = 0

if cnt == 3:
    print("YES")
elif cnt == 2:
    print("MAYBE")
else:
    print("NO")
