N = int(input())

if N >= 42:
    print(f"AGC{N + 1:03}")
else:
    print('AGC' + '0' + str(N))