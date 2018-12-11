from matplotlib import pyplot as pl
from scipy import stats as st

from itertools import islice

import pandas as pd
import numpy as np

from settleddataclass import settled
from autocovariance import auto


directory = '../runs/AlCo/98-2/'
dirfile = directory+'data.txt'

with open(dirfile) as file:
    for line in islice(file, 1, 2):
        values = line.strip().split(' ')
        headers = values[1:]

df = pd.read_csv(dirfile, delimiter=' ', names=headers, skiprows=2)

timestep = 0.001
time = [timestep*i for i in df['TimeStep']]
df['time'] = time

start = None
end = 1000

temp = list(df['c_mytemp'][start:end])
time = list(df['time'][start:end])

k, r, index = auto(temp)
index *= 2  # Double the correlation length

corblocking = settled()

binnedtime = corblocking.batch(time, b=index)
bins = binnedtime[-1]
binnedtime = binnedtime[0]

binnedtemp = corblocking.batch(temp, b=index)[0]
binnedslopes = corblocking.binslopes(binnedtime, binnedtemp, bins)

settledpindex = corblocking.ptest(binnedtemp, 0.05)
settledslopeindex = corblocking.findslopestart(binnedslopes)

slopeoverstdindex = corblocking.slopeoverstd(binnedtemp, binnedslopes)

slopeindex = max([settledslopeindex, settledpindex, slopeoverstdindex])

settledindex = corblocking.finddatastart(binnedtime, slopeindex)

settledpindex = corblocking.ptest(binnedtemp, 0.05)

fig, ax = pl.subplots()

binnumber = list(range(1, len(binnedslopes)+1))
ax.plot(
        binnumber,
        binnedslopes,
        label='Bins='+str(bins),
        marker='.'
        )

ax.plot(
        binnumber[slopeindex],
        binnedslopes[slopeindex],
        label='Settled Start',
        marker='o',
        linestyle='none',
        color='r'
        )

ax.plot(
        binnumber[settledslopeindex],
        binnedslopes[settledslopeindex],
        label='Method: Slope Change',
        marker='*',
        linestyle='none',
        color='g'
        )

ax.plot(
        binnumber[settledpindex],
        binnedslopes[settledpindex],
        label='Method: p-value',
        marker='*',
        linestyle='none',
        color='y'
        )

ax.plot(
        binnumber[slopeoverstdindex],
        binnedslopes[slopeoverstdindex],
        label='Method: slope/std',
        marker='*',
        linestyle='none',
        color='k'
        )

ax.set_xlabel('Number of Bins')
ax.set_ylabel('Slope [K/ps]')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()
fig.savefig('../method')

fig, ax = pl.subplots()
ax.plot(time, temp, linestyle='none', color='r', marker='.', label='Data')
ax.axvline(x=time[settledindex], color='b', linestyle='--', label='Settled Start')

mean = np.mean(temp[settledindex:])
ax.axhline(y=mean, color='k', label='Settled Mean='+str(mean)+' [K]')
ax.set_xlabel('Time [ps]')
ax.set_ylabel('Temperature [K]')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()
fig.savefig('../data')

fig, ax = pl.subplots()
ax.plot(k, r, '.', label='data')
ax.axvline(x=index, color='r', linestyle='--', label='k='+str(index))
ax.set_ylabel('Autocorrelation')
ax.set_xlabel('k-lag')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()
fig.savefig('../autocorrelation')
