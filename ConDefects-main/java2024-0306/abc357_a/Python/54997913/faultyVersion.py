N, M = map(int, input().split())
H = list(map(int, input().split()))

total = M
for i in range(N):
    total -= H[i]
    if total < 0:
        print(i + 1)
        break
else:
    print(N)