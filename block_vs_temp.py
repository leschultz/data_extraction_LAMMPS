from matplotlib import pyplot as pl
from scipy import stats as st

from itertools import islice

import pandas as pd
import numpy as np

from settleddataclass import settled
from autocovariance import auto
from outimport import readdata


directory = '../'
dirfile = directory+'test.out'

df = readdata(dirfile)

timestep = 0.001
time = [timestep*i for i in df['Step']]
df['time'] = time

start = 429
end = 460

temp = list(df['Temp'][start:end])
time = list(df['time'][start:end])
steps = list(df['Step'][start:end])

print('Start step: '+str(steps[0]))
print('End step: '+str(steps[-1]))

k, r, index = auto(temp)

setindexes = settled(time, temp, b=index*2)
binnedtime, binnedtemp = setindexes.batch()

binnedslopes, binnedslopeerr = setindexes.binslopes()

slopebin = setindexes.findslopestart()
pbin = setindexes.ptest()

indexes = setindexes.finddatastart()

settledindex = []
for key in indexes:
    settledindex.append(indexes[key])

settledindex = max(settledindex)

fig, ax = pl.subplots()

binnumber = list(range(1, len(binnedslopes)+1))
averagetemps = [np.mean(i) for i in binnedtemp]
ax.plot(
        binnumber,
        binnedslopes,
        label='Input Block Length(b='+str(index)+')',
        marker='.'
        )

ax.plot(
        binnumber[slopebin],
        binnedslopes[slopebin],
        label='Method: Slope Change',
        marker='*',
        markersize=12,
        linestyle='none',
        color='g'
        )

ax.set_xlabel('Bin')
ax.set_ylabel('Slope [K/ps]')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()
fig.savefig('../slopemethod')

fig, ax = pl.subplots()

ax.plot(
        binnumber,
        averagetemps,
        label='Input Block Length(b='+str(index)+')',
        marker='.'
        )

ax.plot(
        binnumber[pbin],
        averagetemps[pbin],
        label='Method: p-value',
        marker='x',
        markersize=12,
        linestyle='none',
        color='r'
        )

ax.set_xlabel('Bin')
ax.set_ylabel('Average Temperature [K/bin]')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()
fig.savefig('../pmethod')

fig, ax = pl.subplots()

ax.plot(
        binnumber,
        binnumber,
        label='Input Block Length(b='+str(index)+')',
        marker='.'
        )

ax.plot(
        binnumber[pbin],
        binnumber[pbin],
        label='Method: slope/std',
        marker='v',
        markerfacecolor='none',
        markersize=12,
        linestyle='none',
        color='k'
        )

ax.set_xlabel('Bin')
ax.set_ylabel('|Slope/STD| [ps^-1]')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()
fig.savefig('../slopeoverstdmethod')

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
ax.axvline(
           x=index,
           color='r',
           linestyle='--',
           label='Correlation Length (k='+str(index)+')'
           )

ax.set_ylabel('Autocorrelation')
ax.set_xlabel('k-lag')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()
fig.savefig('../autocorrelation')
