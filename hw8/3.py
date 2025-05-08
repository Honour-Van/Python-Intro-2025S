def time_seconds(time1):
    h1, m1, s1 = map(int, time1.split(":"))
    return s1 + m1 * 60 + h1 * 3600

n = int(input())
stat = {}
for i in range(n):
    name, time1, time2 = input().split()
    stat[name] = stat.get(name, 0) + time_seconds(time2) - time_seconds(time1)

print(sorted(stat.items(), key=lambda x: -x[1])[0][0])
