a = [int(i) for i in input().split()]
n = int(input())
for i in range(n):
    action, num = input().split()
    num = int(num)
    if action == "Append":
        a.append(num)
    elif action == "Delete":
        if num < len(a):
            a.pop(num)
    elif action == "Modify":
        if a:
            a[-1] = num
a.sort(reverse=True)
print(' '.join(map(str, a)))
