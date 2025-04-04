card = input()
s = 0

for i in card[::2]:
    a = int(i) * 2
    s += a // 10 + a % 10

for i in card[1:-1:2]:
    s += int(i)

c = s % 10
if c == 0 and int(card[-1]) == 0 or int(card[-1]) == 10 - c:
    print('yes')
else:
    print("no")
