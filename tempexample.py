from matplotlib import pyplot as pl

import itertools as it
import pandas as pd

from infoparser import parameters

directory = '/home/nerve/Desktop/data/4000atom1145000/'
tempfile = directory+'test.out'

runs = parameters('/home/nerve/Desktop/data')
runs.files()
param = runs.inputinfo()
param = param['/home/nerve/Desktop/data/4000atom1145000/uwtraj.lammpstrj']
print(param)

with open(tempfile) as file:
    for line in file:
        values = line.strip().split(' ')
        if values[0] == 'Step':
            headers = values
            break

count = 0
index = []
columns = []
with open(tempfile) as file:
    for line in file:
        values = line.strip().split(' ')
        try:
            numbers = [float(i) for i in values if '' is not i]
            if numbers:
                columns.append(numbers)

        except Exception:
            pass

        if values[0] == 'Step':
            index.append(count)

        count += 1

index = [i-min(index) for i in index]

df = pd.DataFrame(columns)
df.columns = headers

print(df.columns)
print(index)
print(df['Step'])
fig, ax = pl.subplots()

start = None
end = None

ax.plot(df['Step'].iloc[start:end], df['Temp'].iloc[start:end], '.')
ax.set_ylabel('Diffusion MO Percent Error')
ax.set_xlabel('Temperature [K]')
ax.grid()

fig.tight_layout()
pl.show()
