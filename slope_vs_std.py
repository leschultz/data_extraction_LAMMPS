from matplotlib import pyplot as pl
from scipy import stats as st

from itertools import islice

import pandas as pd
import numpy as np
import math

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
end = 1100

temp = df['c_mytemp'][start:end]
t = df['time'][start:end]

temprev = temp[::-1]
trev = t[::-1]

centroid = (sum(t)/len(t), sum(temp)/len(temp))

fig, ax = pl.subplots()
ax.plot(t, temp, 'r.', label='Data')
ax.plot(centroid[0], centroid[1], '*k', label='Centroid')
ax.set_xlabel('Time [ps]')
ax.set_ylabel('Temperature [K]')
ax.legend(loc='best')
ax.grid()
fig.tight_layout()

slopes = []
slopesrev = []
r = []
rrev = []
std = []
stdrev = []
for i in range(2, len(temp)+1):

    fit = st.linregress(t[0:i], temp[0:i])
    fitrev = st.linregress(trev[0:i], temprev[0:i])

    slopes.append(fit[0])
    slopesrev.append(fitrev[0])

    r.append(fit[2])
    rrev.append(fitrev[2])

    std.append(np.std(temp[0:i]))
    stdrev.append(np.std(temprev[0:i]))

fig, ax = pl.subplots()

ax.plot(slopes, '.', label='Normal')
ax.plot(slopesrev, '.', label='Reversed')
ax.set_xlabel('Number of Bins')
ax.set_ylabel('Temperature [K]')
ax.legend(loc='best')
ax.grid()
fig.tight_layout()

pl.show()
