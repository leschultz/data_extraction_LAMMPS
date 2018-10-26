from matplotlib import pyplot as pl

from autocorrelation import *
from block_averaging import block

import numpy as np
import random as rnd

x = [100]*100
x = [i+rnd.randint(-10, 10) for i in x]

for i in range(3, len(x), len(x)//10):
    bl = block(x, i)
    pl.plot(i, bl[1], '.', label='n='+str(i))

mean = np.mean(x)
pl.xlabel('Number of Blocks')
pl.ylabel('Deviation from mean='+str(mean))
pl.legend(loc='best')
pl.tight_layout()
pl.grid()
pl.savefig('../random')
pl.clf()
