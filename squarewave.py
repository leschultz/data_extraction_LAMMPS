'''https://emcee.readthedocs.io/en/latest/tutorials/autocorr/'''

from matplotlib import pyplot as pl
from scipy import stats as st
from scipy import signal
import numpy as np
import math

from asymptoticvariance import error as asymp
from stationary import error as staerr
from batchmeans import error as batch
from autocoverr import error as new
from autocovariance import auto

x = np.linspace(0, 10, 10)
y = signal.square(x)
mean = sum(y)/len(y)

k, r, last = auto(y)
err = staerr(y, math.floor(len(x)**0.5))

print(st.sem(y))
print(err[0])
print(new(y, math.floor(len(y)**0.5))[0])
print(batch(y))
print(((((1-0)**2+(-1-0)**2+(1-0)**2+(-1-0)**2)/(4-1))**0.5)/(4**0.5))

pl.plot(x, y, '.', label='Mean = '+str(mean))
pl.xlabel('x-point')
pl.ylabel('y-point')
pl.grid()
pl.legend(loc='best')
pl.savefig('../square')
pl.clf()

pl.plot(k, r)
pl.xlabel('Lag-k')
pl.ylabel('Autocorrelation')
pl.grid()
pl.savefig('../squareauto')
pl.clf()
