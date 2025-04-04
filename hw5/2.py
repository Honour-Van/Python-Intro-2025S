n = int(input())
gold, silver, bronze = 0, 0, 0
for i in range(n):
    a, b, c = map(int, input().split())
    gold += a
    silver += b
    bronze += c
print(gold, silver, bronze, gold + silver + bronze)
