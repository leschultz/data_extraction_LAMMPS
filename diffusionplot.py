from matplotlib import pyplot as pl
from diffusionimport import load

import os

mo = '../datacalculated/diffusion/'
image = '../images/diffusion/'

files = os.listdir(mo)

names = []
runset = []
for item in files:
    if '_origins' in item:
        names.append(item)
        runset.append(item.split('_')[0])

runset = list(set(runset))

for run in runset:
    points = {}
    for name in names:
        data = load(mo+name)

        time = data['start_time']

        del data['start_time']

        temp = float(name.split('origins_')[1])
        for key in data:
            if '_Err' not in key:
                pl.plot(time, data[key], marker='.', label=key)

                pl.xlabel('Start Time [ps]')
                pl.ylabel('Diffusion [*10^-4 cm^2 s^-1]')
                pl.grid(b=True, which='both')
                pl.legend(loc='best')
                pl.tight_layout()
                pl.savefig(image+name+'_'+key)
                pl.clf()

                if 'all' in key:
                    points[temp] = data[key]

    for key in points:
        for item in points[key]:
            pl.plot(key, item, marker='.', color='b')

    pl.xlabel('Temperature [K]')
    pl.ylabel('Diffusion [*10^-4 cm^2 s^-1]')
    pl.grid(b=True, which='both')
    pl.tight_layout()
    pl.savefig(image+run)
