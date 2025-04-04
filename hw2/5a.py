speed = int(input())
ride = int(input())
water = int(input())

count = 0
if speed > 15:
    count += 1
if ride > 30:
    count += 1
if 0 <= water <= 5:
    count += 1

# if water == -1:
#     print("NO")
# else:
#     if count == 3:
#         print("YES")
#     elif count == 2:
#         print("MAYBE")
#     else:
#         print("NO")
if water == -1:
    print("NO")
    exit(0)
if count == 3:
    print("YES")
elif count == 2:
    print("MAYBE")
else:
    print("NO")
