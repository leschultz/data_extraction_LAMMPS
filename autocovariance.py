def rho(x, mean, n, k):
    numerator = 0.0
    for i in range(0, n-k):
        numerator += (x[i]-mean)*(x[i+k]-mean)

    denominator = 0.0
    for i in range(0, n):
        denominator += (x[i]-mean)**2.0

    normcor = numerator/denominator

    return normcor


def auto(x):
    n = len(x)
    mean = sum(x)/n

    k = []
    r = []
    for i in range(0, n):
        k.append(i)
        r.append(rho(x, mean, n, i))

    count = 0
    for i in r:
        if i >= 0.0:
            last = count
            count += 1
        else:
            break

    if last == 0:
        last += 1

    return k, r, last
