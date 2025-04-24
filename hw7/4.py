from datetime import datetime
enter_time = {}
time_count = {}

def time_seconds(time1):
    h1, m1, s1 = map(int, time1.split(":"))
    return s1 + m1 * 60 + h1 * 3600

while True:
    line = input()
    if line == "QUIT":
        break
    name, time = line.split(',')
    enter_time[name] = enter_time.get(name, []) + [time_seconds(time)]

for k, v in enter_time.items():
    l = sorted(v)
    for i in range(0, len(l), 2):
        time_count[k] = time_count.get(k, 0) + l[i+1] - l[i]

for k, v in sorted(time_count.items(), key=lambda x: -x[1]):
    print(f"{k},{v}")