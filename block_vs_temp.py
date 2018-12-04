from matplotlib import pyplot as pl
from itertools import islice

import pandas as pd
import numpy as np


def batch(x, a=None, b=None):
    n = len(x)
    mean = sum(x)/n

    if a is None:
        a = n//b

    if b is None:
        b = n//a

    blocks = np.array_split(x, a)
    for i in blocks:
        print(i)

    return np.array_split(x, a)

directory = '../runs/AlCo/98-2/'
dirfile = directory+'data.txt'

with open(dirfile) as file:
    for line in islice(file, 1, 2):
        values = line.strip().split(' ')
        headers = values[1:]

df = pd.read_csv(dirfile, delimiter=' ', names=headers, skiprows=2)

start = None
end = 1100

start = 950
end = 1000

temp = list(df['c_mytemp'][start:end])
step = list(df['TimeStep'][start:end])

fig, ax = pl.subplots()
ax.plot(step, temp, 'r.')
ax.set_xlabel('Timestep')
ax.set_ylabel('Temperature [K]')
ax.grid()
fig.tight_layout()

print(sum(step))

data = {}
a = [1, 10, 20, 30]
for i in a:
    print('a='+str(i))

    x = batch(step, b=i)
    print(sum([sum(i) for i in x]))

'''

fig, ax = pl.subplots()

for key in data:
    ax.plot(data[key], label=key, marker='.')

ax.set_xlabel('Number of Bins')
ax.set_ylabel('Temperature [K]')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()

pl.show()

'''
