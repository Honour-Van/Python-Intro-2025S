score = int(input())


if score < 60:
    gpa = 0
elif score == 100:
    gpa = 4.00
elif score == 60:
    gpa = 1.00
else:
    gpa = 4 - 3 * ((100 - score) ** 2) / 1600


print("{0:.2f}".format(gpa))
