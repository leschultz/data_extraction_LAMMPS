from matplotlib import pyplot as pl
from scipy import stats as st

from itertools import islice

import pandas as pd
import numpy as np

from autocovariance import auto


def batch(x, a=None, b=None):
    n = len(x)

    if a is None:
        a = n//b

    if b is None:
        b = n//a

    blocks = np.array_split(x, a)

    return blocks, a


def blockdata(y, *args, **kwargs):
    x, bins = batch(y, *args, **kwargs)

    std = []
    for j in range(0, len(x)):
        std.append(np.std(x[j]))

    return std, bins, x


def endfinder(x):
    n = len(x)-1

    for i in range(0, n):
        diff = x[i+1]-x[i]
        if diff > 0.0:
            break

    for j in range(n, 1, -1):
        diff = x[j-1]-x[j]
        if diff > 0.0:
            break

    return i, j


def findindexes(x, i0, j0):
    i1 = sum([len(i) for i in x[:i0]])
    i2 = sum([len(i) for i in x[:j0]])

    return i1, i2


directory = '../runs/AlCo/98-2/'
dirfile = directory+'data.txt'

with open(dirfile) as file:
    for line in islice(file, 1, 2):
        values = line.strip().split(' ')
        headers = values[1:]

df = pd.read_csv(dirfile, delimiter=' ', names=headers, skiprows=2)

timestep = 0.001
time = [timestep*i for i in df['TimeStep']]
df['time'] = time

start = None
end = 1100

start = 300
end = 1100

start = 300
end = 1000


temp = list(df['c_mytemp'][start:end])
time = list(df['time'][start:end])

k, r, index = auto(temp)

data = {}
corblocking = blockdata(temp, b=index)
data[corblocking[1]] = corblocking[0]

fig, ax = pl.subplots()

for key in data:

    i0, j0 = endfinder(data[key])

    indexes = findindexes(corblocking[2], i0, j0)
    
    x = np.array(list(range(1, key+1)))
    y = np.array(data[key])

    ax.plot(
            x,
            y,
            label='Bins='+str(key),
            marker='.'
            )

    ax.plot(
            x[[i0, j0]],
            y[[i0, j0]],
            label='Settled Range',
            marker='o',
            color='r'
            )

ax.set_xlabel('Number of Bins')
ax.set_ylabel('Temperature STD [K]')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()

fig, ax = pl.subplots()
ax.plot(time, temp, linestyle='none', color='r', marker='.', label='Data')
ax.axvline(x=time[indexes[0]], color='g', linestyle='--', label='Settled Start')
ax.axvline(x=time[indexes[1]], color='b', linestyle='--', label='Settled End')

mean = np.mean(temp[indexes[0]:indexes[1]])
ax.axhline(y=mean, color='k', label='Settled Mean='+str(mean))
ax.set_xlabel('Time [ps]')
ax.set_ylabel('Temperature [K]')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()

fig, ax = pl.subplots()
ax.plot(k, r, '.', label='data')
ax.axvline(x=index, color='r', linestyle='--', label='k='+str(index))
ax.set_ylabel('Autocorrelation')
ax.set_xlabel('k-lag')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()

pl.show()
