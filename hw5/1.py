a = [float(x) for x in input().split()]
a = list(map(lambda x : min(x, 10), filter(lambda x : x > 2, a)))

if len(a) >= 10 and sum(a) >= 85:
    print("PASS")
else:
    print("FAIL")
