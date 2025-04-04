N, M = map(int, input().split(":"))

if N > M:
    N, M = M, N

is_prime = [True] * (M + 1)
is_prime[0] = False
is_prime[1] = False

def sift():
    for i in range(2, M + 1):
        for j in range(2 * i, M + 1, i):
            is_prime[j] = False

def getPrime():
    def checkPrime(n):
        if n == 0 or n == 1:
            return False
        l = int(n ** 0.5)
        for i in range(2, l + 1):
            if n % i == 0:
                return False
        return True
    for i in range(M + 1):
        is_prime[i] = checkPrime(i)

# sift()
getPrime()

# print(is_prime)

for i in range(N, M - 1):
    if is_prime[i] and is_prime[i + 2]:
        print(f'{i};{i+2}')
