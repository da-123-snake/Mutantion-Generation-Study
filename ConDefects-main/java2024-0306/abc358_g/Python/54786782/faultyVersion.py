import bisect
import collections
import functools
import heapq
import itertools
import math
import operator
import string
import sys
import typing
# sys.setrecursionlimit(1000000)

readline = sys.stdin.readline
LS = lambda: readline()
LI = lambda: int(readline())
LLS = lambda: readline().split()
LL = lambda: list(map(int, readline().split()))

h, w, k = LL()
sx, sy = LL()
sx -= 1
sy -= 1
A = [LL() for _ in range(h)]

moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
f = [[[float("-inf")] * w for _ in range(h)] for _ in range(min(k, h * w) + 2)]
f[0][sx][sy] = 0
res = 0
for i in range(min(k, h * w) + 1):
    for hh in range(h):
        for ww in range(w):
            res = max(res, f[i][hh][ww] + A[hh][ww] * (k - i))
            for dh, dw in moves:
                nh, nw = hh + dh, ww + dw
                if 0 <= nh < h and 0 <= nw < w:
                    f[i + 1][nh][nw] = max(f[i + 1][nh][nw], f[i][hh][ww] + A[hh][ww])
print(res)
