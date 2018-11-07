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

x = np.linspace(0, 100, 1000)
y = np.sin(x)
mean = sum(y)/len(y)

k, r, last = auto(y)
err = staerr(y, math.floor(len(x)**0.5))

print(st.sem(y))
print(err)
print(new(y, math.floor(len(y)**0.5)))
print(batch(y))

pl.plot(x, y, label='Mean = '+str(mean))
pl.xlabel('x-point')
pl.ylabel('y-point')
pl.grid()
pl.legend(loc='best')
pl.savefig('../sine')
pl.clf()

pl.plot(k, r)
pl.xlabel('Lag-k')
pl.ylabel('Autocorrelation')
pl.grid()
pl.savefig('../sineauto')
pl.clf()
