'''https://emcee.readthedocs.io/en/latest/tutorials/autocorr/'''


from matplotlib import pyplot as pl
from scipy import stats as st
from itertools import islice
import numpy as np
import math

from asymptoticvariance import error as asymp
from batchmeans import error as batch
from autocovariance import auto
from stationary import error as staerr

step = []
temp = []
with open('../data.txt') as file:
    for line in islice(file, 2, None):
        values = line.strip().split(' ')
        values = [float(i) for i in values]
        step.append(values[0])
        temp.append(values[1])

start = 10000
stop = None
skip = 100
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

pl.plot(k, r, '.b')
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
lengths = [10, 100, 1000]
lengths += [50, 500, 5000]
lengths += [25, 250, 2500]
lengths += [75, 750, 7500]
lengths += [400, 650]
for i in lengths:
    print('Data Length: '+str(i))
    data = temp[:i]
    x.append(len(data)*skip)
    y.append(batch(data))
    w.append(staerr(data))
    z.append(asymp(data))
    u.append(np.std(data))

pl.plot(x, y, '.b', label='Batch Means')
pl.plot(x, z, '.r', label='General Formula')
pl.plot(x, w, '.k', label='Stationary Time Series')
pl.plot(x, u, 'xy', label='Standard Deviation')
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

lengths = [10, 100, 1000]
lengths += [50, 500, 5000]
lengths += [25, 250, 2500]
lengths += [75, 750, 7500]
lengths += [400, 650]
for i in lengths:
    print('Data Length: '+str(i))
    data = temp[:i]
    x.append(len(data)*skip)
    y.append(staerr(data))
    z.append(staerr(data, last))
    w.append(staerr(data, newlast))

pl.plot(x, y, '.b', label='Not Truncated')
pl.plot(x, z, '*r', label='Truncated at k='+str(last))
pl.plot(x, z, 'xk', label='Truncated at k='+str(newlast))
pl.xlabel('Data Length')
pl.ylabel('Error [K]')
pl.tight_layout()
pl.legend(loc='best')
pl.grid()
pl.savefig('../cutuncut')
pl.clf()
