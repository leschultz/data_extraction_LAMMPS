from matplotlib import pyplot as pl
from scipy import stats as st

from itertools import islice

import pandas as pd
import numpy as np

from settleddataclass import settled
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

setindexes = settled(time, temp)
index = setindexes.binsize()
binnedtime, binnedtemp = setindexes.batch()

setindexes.binslopes()

binnedslopes, slopebin = setindexes.slopetest()
pvals, pbin = setindexes.ptest()

slopeerr, slopeerrbin, = setindexes.fittest()

indexes = setindexes.finddatastart()

settledindex = []
for key in indexes:
    if isinstance(indexes[key], int):
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

try:
    ax.plot(
            binnumber[slopebin],
            binnedslopes[slopebin],
            label='Method: Slope Change',
            marker='*',
            markersize=12,
            linestyle='none',
            color='g'
            )

except Exception:
    ax.plot(
            binnumber[-1],
            binnedslopes[-1],
            label='Method: Slope Change Not Settled',
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
        pvals,
        label='Input Block Length(b='+str(index)+')',
        marker='.'
        )

try:
    ax.plot(
            binnumber[pbin],
            pvals[pbin],
            label='Method: p-value Not Settled',
            marker='x',
            markersize=12,
            linestyle='none',
            color='r'
            )

except Exception:
    ax.plot(
            binnumber[-1],
            pvals[-1],
            label='Method: p-value Not Settled',
            marker='x',
            markersize=12,
            linestyle='none',
            color='r'
            )

ax.set_xlabel('Bin')
ax.set_ylabel('p-value')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()
fig.savefig('../pmethod')

fig, ax = pl.subplots()

ax.plot(
        binnumber,
        slopeerr,
        label='Input Block Length(b='+str(index)+')',
        marker='.'
        )

try:
    ax.plot(
            binnumber[slopeerrbin],
            slopeerr[slopeerrbin],
            label='Method: Fit Error Not Settled',
            marker='^',
            markersize=12,
            linestyle='none',
            color='y'
            )

except Exception:
    ax.plot(
            binnumber[-1],
            slopeerr[-1],
            label='Method: Fit Error Not Settled',
            marker='^',
            markersize=12,
            linestyle='none',
            color='y'
            )

ax.set_xlabel('Bin')
ax.set_ylabel('Linear Fit Error [K/ps]')
ax.grid()
ax.legend(loc='best')
fig.tight_layout()
fig.savefig('../fiterror')

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
