'''https://emcee.readthedocs.io/en/latest/tutorials/autocorr/'''

from matplotlib import pyplot as pl
from scipy import stats as st
from scipy import signal
import numpy as np
import math

from asymptoticvariance import error as asymp
from stationary import error as staerr
from batchmeans import error as batch
from autocovariance import auto

x = np.linspace(0, 10, 1000)
y = signal.square(x)

k, r, last = auto(y)
err, gamma0, gammak = staerr(y, math.floor(len(x)**0.5))

print(st.sem(y))
print(err)
print(last)

pl.plot(x, y)
pl.show()
pl.clf()

pl.plot(k, r)
pl.show()
pl.clf()

pl.plot(gammak)
pl.show()
pl.clf()
