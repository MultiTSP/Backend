import numpy as np
import math

inf = 1000000000000000000


def travel_time(coordinates, i, j, speed):
    x1 = coordinates[i][0]
    y1 = coordinates[i][1]
    x2 = coordinates[j][0]
    y2 = coordinates[j][1]
    dis = (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
    dis = math.sqrt(dis)
    dis /= speed
    return dis


def Rk(k, n, m):
    if k == 0:
        return [0, 0]
    if k == n-1:
        return [1, m]
    return [1, min(k, m-1)]


def split(coordinates, n, m, speed):
    sequence = []
    for i in range(1, n):
        sequence.append(i)
    V = np.full((n, m + 1), np.inf)
    V[0, 0] = 0
    P = np.full((n, m + 1), -1, dtype=int)
    for k in range(1, n):
        R = Rk(k-1, n, m)
        for r in range(R[0], R[1]+1):
            if V[k-1, r] < np.inf:
                T = 0
                for j in range(k, n):
                    if k == j:
                        T = travel_time(coordinates,
                                        0, sequence[j-1], speed)+travel_time(coordinates, sequence[j-1], 0, speed)
                    else:
                        T = T-travel_time(coordinates, sequence[j-2], 0, speed)+travel_time(coordinates,
                                                                                            sequence[j-2], sequence[j-1], speed)+travel_time(coordinates, sequence[j-1], 0, speed)
                    _R = Rk(j, n, m)
                    if r+1 >= _R[0] and r+1 <= _R[1] and (max(T, V[k-1, r]) < V[j, r+1]):
                        V[j, r+1] = max(T, V[k-1, r])
                        P[j, r+1] = k-1
    delimiters = []
    r = m
    k = n-1
    while k > 0:
        delimiters.append(k)
        k = P[k, r]
        r -= 1
    t = V[n-1, m]
    answer = [[0]]
    for i in sequence:
        answer[-1].append(i)
        if delimiters[-1] == i:
            delimiters.pop()
            answer[-1].append(0)
            if (len(delimiters) != 0):
                answer.append([0])

    print(t)
    cost = 0

    def func(a):
        c = 0
        for j in range(len(a)-2):
            c += travel_time(coordinates,
                             a[j], a[j+1], speed)
        return c

    for i in range(len(answer)):
        print("i->", i)
        a = answer[i]
        c1 = func(a)
        a.reverse()
        c2 = func(a)
        a.reverse()
        if c2 < c1:
            a.reverse()
        cost = max(cost, min(c1, c2))
    print("cost", cost)
    return [answer, cost]
# append 0 by yourself


# for a given time minimize m
def mtsp(coordinates, time, speed):
    n = len(coordinates)
    start = 1
    end = n
    m = -1
    answer = []
    duration = -1
    while start <= end:
        mid = (start+end)//2
        ans = split(coordinates, n, mid, speed)
        if ans[1] <= time:
            m = mid
            answer = ans[0]
            end = mid-1
            duration = ans[1]
        else:
            start = mid+1
    temp = []
    for i in range(len(answer)):
        temp.append([])
        for j in range(len(answer[i])):
            temp[-1].append(coordinates[answer[i][j]])
    answer = temp
    return [m, answer, duration]