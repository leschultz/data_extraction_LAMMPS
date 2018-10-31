'''
This method used the batch means.
The choice of l can be set as high as 30.
l = 10 is a safe choice.
'''


def batch(x, k, l):
    val = 0.0
    for i in range((k-1)*l+1, k*l):
        val += x[i]

    val /= l

    return val


def batchmean(x, l=10):

    length = len(x)
    m = length*l

    blocks = []
    for i in range(0, m-1):
        blocks.append(batch(x, i, l))

    return blocks
