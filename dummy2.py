'''https://emcee.readthedocs.io/en/latest/tutorials/autocorr/'''

from matplotlib import pyplot as pl
from scipy import stats as st
from itertools import islice
from celerite import terms
import numpy as np
import celerite
import math

from asymptoticvariance import error as asymp
from batchmeans import error as batch
from autocovariance import auto
from stationary import error as staerr
from autocoverr import error as etest

np.random.seed(1234)

# Build the model
kernel = terms.RealTerm(log_a=0.0, log_c=-6.0)
kernel += terms.RealTerm(log_a=0.0, log_c=-2.0)

# The true autocorrelation time can be calculated analytically:
true_tau = sum(2*np.exp(t.log_a-t.log_c) for t in kernel.terms)
true_tau /= sum(np.exp(t.log_a) for t in kernel.terms)
print(true_tau)

# Simulate a set of chains:
points = 10000
gp = celerite.GP(kernel)
t = np.arange(points)
gp.compute(t)
y = gp.sample(size=32)

temp = y[3]
n = len(temp)
step = list(range(0, n))

meantemp = sum(temp)/len(temp)
pl.plot(
        step,
        temp,
        label='Mean: '+str(meantemp)
        )

pl.legend(loc='best')
pl.xlabel('Step [-]')
pl.ylabel('Temperature [K]')
pl.tight_layout()
pl.grid()
pl.savefig('../data')
pl.clf()

x = []
y = []
u = []
lengths = list(range(points//10, points, points//10))
for i in lengths:
    print('Data Length: '+str(i))
    data = temp[:i]
    x.append(len(data))
    y.append(etest(data, math.floor(n**0.5)))
    u.append(st.sem(data))

pl.plot(x, y, '+r', label='Test')
pl.plot(x, u, 'xy', label='Independent SEM')
pl.xlabel('Data Length [steps]')
pl.ylabel('Error [K]')
pl.tight_layout()
pl.legend(loc='best')
pl.grid()
pl.savefig('../convergence')
pl.clf()
