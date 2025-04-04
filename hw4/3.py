n = int(input())

def getBMI(h, w):
    bmi = w / ((h / 100) ** 2)
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24:
        return "Normal"
    elif bmi < 28:
        return "Overweight"
    else:
        return "Obesity"

for i in range(n):
    height,weight = map(float, input().split())
    result = getBMI(height,weight)
    print(result)
