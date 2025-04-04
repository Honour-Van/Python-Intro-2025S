cash = 0
saving = 0

out_of_cash = False
for i in range(1, 12 + 1):
    cost = int(input())
    if out_of_cash:
        continue
    cash += 300
    cash -= cost
    if cash < 0:
        print(-i)
        out_of_cash = True
        continue
    saving_cnt = cash // 100
    if saving_cnt:
        cash -= saving_cnt * 100
        saving += saving_cnt * 100
if not out_of_cash:
    print(int(saving * 1.2 + cash))
