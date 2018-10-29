'''https://emcee.readthedocs.io/en/latest/tutorials/autocorr/'''


from matplotlib import pyplot as pl

from autocorrelation import *
from block_averaging import block

import numpy as np

# Build the celerite model:
import celerite
from celerite import terms
kernel = terms.RealTerm(log_a=0.0, log_c=-6.0)
kernel += terms.RealTerm(log_a=0.0, log_c=-2.0)

# Simulate a set of chains:
gp = celerite.GP(kernel)
t = np.arange(100)
gp.compute(t)
y = gp.sample(size=32)
data = y[3]

data = [i+100 for i in data]

pl.plot(data)
pl.ylabel('Random Markov Chain')
pl.xlabel('Index')
pl.tight_layout()
pl.grid()
pl.show()
pl.clf()

print(block(data))
a, index, values = autoerror(data)
print(a)

pl.plot(index, values, '.')
pl.ylabel('Autocorrelation')
pl.xlabel('Index')
pl.tight_layout()
pl.grid()
pl.show()
pl.clf()
