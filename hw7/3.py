n = int(input())
if n == 1:
    print([1])
else:
    last_list = [1]
    print([1])
    for i in range(2, n+1):
        cur_list = [i] * i
        for j in range(1, i-1):
            cur_list[j] = last_list[j-1] + last_list[j]
        last_list = cur_list
        print(cur_list)