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

x = np.linspace(0, 50*math.pi, 1000)
y = np.sin(x)
mean = sum(y)/len(y)

k, r, last = auto(y)
err, gammastat0, gammastatk, kerr = staerr(y)
errnew, gammanew0, gammanewk, jerr = new(y)

print(st.sem(y))
print(err)
print(errnew)
print(batch(y))

pl.plot(x, y, label='Mean = '+str(mean))
pl.xlabel('x-point')
pl.ylabel('y-point')
pl.grid()
pl.legend(loc='best')
pl.savefig('../sine')
pl.clf()

pl.plot(kerr, gammastatk, label='gamma0='+str(gammastat0) +' for handbook')
pl.plot(jerr, gammanewk, label='gamma0='+str(gammanew0)+' for Ukui')
pl.xlabel('Lag-k')
pl.ylabel('gamma_k sum')
pl.grid()
pl.legend(loc='best')
pl.savefig('../sinegamma')
pl.clf()

pl.plot(k, r, label='k before first 0 is: '+str(last))
pl.xlabel('Lag-k')
pl.ylabel('Autocorrelation')
pl.grid()
pl.legend(loc='best')
pl.savefig('../sineauto')
pl.clf()
