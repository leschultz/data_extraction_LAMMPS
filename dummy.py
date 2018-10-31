'''https://emcee.readthedocs.io/en/latest/tutorials/autocorr/'''


from matplotlib import pyplot as pl
from scipy import stats as st
from itertools import islice

from overlappingbatchmeans import *
from autocorrelation import *
from block_averaging import *
from batchmeans import batchmean
from chainerror import *

import numpy as np

step = []
temp = []
with open('../data.txt') as file:
    for line in islice(file, 2, None):
        values = line.strip().split(' ')
        values = [float(i) for i in values]
        step.append(values[0])
        temp.append(values[1])

start = 10000
stop = None  # start+6801*5
step = step[start:stop]
temp = temp[start:stop]
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
#pl.show()
pl.clf()

period = 6800

'''
var = block(temp, n)
print('Block error blocks=n: '+str(var[1]))

var = block(temp, 300)
print('Block error blocks~sqrt(n): '+str(var[1]))
'''
var = block(temp, 10)
print('Block error blocks=10: '+str(var[1]))
'''
a = autoerror(temp)
print('Variance (from formula): '+str(a))

a = error(temp)
print('Time estimate error: '+str(a))

print('Scipy SEM: '+str(st.sem(temp)))
'''

print(errorchain(temp, period))
print(other(temp, period))
print(np.std(temp))

'''
values = []
for i in range(0, n):
    values.append(normautocor(temp[::10], i))

pl.plot(step, values, '.')
pl.ylabel('Autocorrelation')
pl.xlabel('Step')
pl.tight_layout()
pl.grid()
#pl.show()
pl.clf()'''
