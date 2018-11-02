'''https://emcee.readthedocs.io/en/latest/tutorials/autocorr/'''


from matplotlib import pyplot as pl
from scipy import stats as st
from itertools import islice

from asymptoticvariance import error as asymp 
from batchmeans import error as batch
from block_averaging import block
from autocorrelation import *

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
stop = start + 6801*5
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
# pl.show()
pl.clf()

# print(asymp(temp, period))
print('Scipy SEM: '+str(st.sem(temp)))
print('Batch Means Error a=10: '+str(batch(temp, 10)))
print('General Formula Error: '+str(asymp(temp)))


'''
x = []
y = []
for i in range(1, n, 100):
    x.append(i)
    y.append(batch(temp, i))

pl.plot(x, y, '.b')
print(y[-1])
pl.show()
'''
'''
index = []
values = []
for i in range(0, n):
    index.append(i)
    values.append(normautocor(temp, i))

pl.plot(index, values, '.')
pl.ylabel('Autocorrelation')
pl.xlabel('Step')
pl.tight_layout()
pl.grid()
pl.show()
pl.clf()'''
