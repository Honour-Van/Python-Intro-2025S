village_status = input()
status_list = list(village_status)
length = len(status_list)

for i in range(length):
    if village_status[i] == '*':
        # 向左传播
        if i > 0:
            status_list[i - 1] = '*'
        # 向右传播
        if i < length - 1:
            status_list[i + 1] = '*'

virus_count = status_list.count('#')
print(virus_count)