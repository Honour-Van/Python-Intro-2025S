
def gpa(score):
    return 4 - 3 * (100 - score) ** 2 / 1600 if score >= 60 else 0

n = int(input())
d = dict()
for i in range(n):
    l = input().split()
    stu = l[0]
    c = len(l)
    score_sum = 0
    gpa_sum = 0
    for x in range(1, c, 2):
        y = x + 1
        gpa_sum += gpa(float(l[x])) * int(l[y])
        score_sum += int(l[y])
    d[stu] = gpa_sum / score_sum

for k, v in sorted(d.items(), key=lambda x : x[1], reverse=True):
    print(k)