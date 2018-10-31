'''
This method used the overlapping batch means.
The choice of l need to be good for this to work.
'''

def overlapmean(x, l, j):
    val = 0.0
    for i in range(j, j+l-1):
        val += x[i]
    val /= l

    return val


def batch(x, l=10):
    length = len(x)
    mean = sum(x)/length

    # Divide the data into blocks
    blocks = [x[i::l] for i in range(l)]

    blocklength = len(blocks)
    term = blocklength-l+1

    val = 0.0
    for i in range(0, term):
        val += (overlapmean(blocks[i], l, i)-mean)**2.0

    val /= term
    val *= l

    sigma = val**0.5
    sem = sigma/blocklength**0.5

    return sem
