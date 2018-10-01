from matplotlib import pyplot as pl

import os

directory = '../datacalculated/msd/'

names = os.listdir(directory)

runs = []
for item in names:
    if 'run1' in item:

        runs.append(item)

labels = []
data = {}
for name in runs:

    temp = name.split('K-')[1]
    labels.append(temp.split('_')[0])

    if data.get(name) is None:
        data[name+'_time'] = []
        data[name+'_msd'] = []
        data[name+'_err'] = []

    with open(directory+name) as file:
        next(file)
        for line in file:
            value = line.split(',')
            data[name+'_time'].append(float(value[0]))
            data[name+'_msd'].append(float(value[1]))
            data[name+'_err'].append(float(value[2]))

for key in runs:
    if '_time' in key:

        pl.errorbar(data[key+'_time'], data[key+'_msd'], data[key+'_err'])


pl.xlabel('Time [ps]')
pl.ylabel('Mean Squared Displacement [A^2]')
pl.grid(b=True, which='both')
pl.tight_layout()
pl.legend(labels, loc='best')
pl.savefig('MSD')
pl.clf()
