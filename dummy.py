'''https://emcee.readthedocs.io/en/latest/tutorials/autocorr/'''


from matplotlib import pyplot as pl
from scipy import stats as st
from itertools import islice
import numpy as np

from asymptoticvariance import error as asymp 
from batchmeans import error as batch

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

print('Scipy SEM: '+str(st.sem(temp)))
print('Batch Means Error (a=10): '+str(batch(temp, 10)))
print('General Formula Error: '+str(asymp(temp)))

x = []
y = []
z = []
lengths = [10, 100, 1000]
lengths += [50, 500, 5000]
lengths += [25, 250, 2500]
lengths += [75, 750, 7500]
for i in lengths:
    print('Data Length: '+str(i))
    data = temp[:i]
    x.append(len(data)*skip)
    y.append(batch(data))
    z.append(asymp(data))

pl.plot(x, y, '.b', label='Batch Means')
pl.plot(x, z, '.r', label='General Formula')
pl.xlabel('Data Length')
pl.ylabel('Error [K]')
pl.tight_layout()
pl.legend(loc='best')
pl.grid()
pl.savefig('../convergence')
pl.clf()
