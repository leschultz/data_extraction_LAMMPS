'''https://emcee.readthedocs.io/en/latest/tutorials/autocorr/'''


from matplotlib import pyplot as pl
from scipy import stats as st
from itertools import islice
import numpy as np
import math

from batchmeans import error as batch
from autocovariance import auto
from stationary import error as staerr
from autocoverr import error as asymp

step = []
temp = []
with open('../nve.txt') as file:
    for line in islice(file, 2, None):
        values = line.strip().split(' ')
        values = [float(i) for i in values]
        step.append(values[0])
        temp.append(values[1])

start = 10000
stop = None
skip = 1000
period = 6800

step = step[start:stop:skip]
temp = temp[start:stop:skip]
n = len(temp)

meantemp = sum(temp)/len(temp)
pl.plot(
        step,
        temp,
        label='Mean Temperature: '+str(meantemp)+' [K]'
        )

pl.legend(loc='best')
pl.xlabel('Step [-]')
pl.ylabel('Temperature [K]')
pl.tight_layout()
pl.grid()
pl.savefig('../data')
pl.clf()

k, r, last = auto(temp)

pl.plot(k, r)
pl.xlabel('Lag-k')
pl.ylabel('Autocovrrelation')
pl.tight_layout()
pl.legend(['Last k before zero: '+str(last)], loc='best')
pl.grid()
pl.savefig('../auto')
pl.clf()

x = []
y = []
z = []
w = []
u = []
g = []
lengths = list(range(n//10, n, n//10))
batches = 5
for i in lengths:
    print('Data Length: '+str(i))
    data = temp[:i]
    x.append(len(data))
    y.append(batch(data, batches))
    g.append(batch(data))
    w.append(staerr(data)[0])
    z.append(asymp(data)[0])
    u.append(st.sem(data))

pl.plot(x, y, '.b', label='Batch Means (a='+str(batches)+')')
pl.plot(x, g, '*b', label='Batch Means (b='+str(math.floor(n**0.5))+')')
pl.plot(x, z, '+r', label='Ukui Estimator')
pl.plot(x, w, '.k', label='Handbook Estimator')
pl.plot(x, u, 'xy', label='Independent SEM')
pl.xlabel('Data Length [steps]')
pl.ylabel('Error [K]')
pl.tight_layout()
pl.legend(loc='best')
pl.grid()
pl.savefig('../convergence')
pl.clf()

x = []
y = []
z = []
w = []
newlast = math.floor(n**0.5)

lengths = list(range(n//10, n, n//10))
for i in lengths:
    print('Data Length: '+str(i))
    data = temp[:i]
    x.append(len(data))
    y.append(staerr(data)[0])
    z.append(staerr(data, last)[0])
    w.append(staerr(data, newlast)[0])

pl.plot(x, y, '.b', label='Not Truncated')
pl.plot(x, z, '*r', label='Truncated at k='+str(last))
pl.plot(x, w, 'xk', label='Truncated at k='+str(newlast))
pl.plot(x, u, 'xy', label='Independent SEM')
pl.xlabel('Data Length')
pl.ylabel('Error [K]')
pl.tight_layout()
pl.legend(loc='best')
pl.grid()
pl.savefig('../cutuncut')
pl.clf()

blocksizes = list(range(2, 30))
err = []
for size in blocksizes:
    err.append(batch(temp, size))

pl.plot(blocksizes, err, '.b')
pl.xlabel('Number of Blocks')
pl.ylabel('Error [K]')
pl.tight_layout()
pl.grid()
pl.savefig('../varyblock')
pl.clf()

