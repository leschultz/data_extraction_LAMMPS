from scipy.interpolate import UnivariateSpline
from matplotlib import pyplot as pl
import pandas as pd
import numpy as np
import math
import re

from dataimport import importdata as data
from parmimport import importparm as parm


def function(E, T):
    kb = 8.6173303e-5  # [eV/K]
    return E-3.0*kb*T

param = parm()
keys = list(param.keys())
runs = data(int(param[keys[0]]['hold']/param[keys[0]]['rate'])+500)

almass = 4.4803895e-23  # [g]
smmass = 2.4967863e-22  # [g]
comass = 9.7860864e-23  # [g]
nimass = 9.7462675e-23  # [g]
femass = 9.2732796e-23  # [g]
nbmass = 1.5427466e-22  # [g]
timass = 7.9485017e-23  # [g]

masses = {
          'Al': almass,
          'Sm': smmass,
          'Co': comass,
          'Ni': nimass,
          'Fe': femass,
          'Nb': nbmass,
          'Ti': timass
          }

for run in runs:
    print('volume: '+run)

    runs[run] = runs[run].sort_values(by='c_mytemp', ascending=True)

    parse = run.split('_')
    ratio = parse[-1]
    ratio = ratio.split('-')
    ratio = [float(i)/100 for i in ratio]

    elements = re.findall('[A-Z][a-z]*', parse[0])

    volume = runs[run]['v_myvol']

    ratios = dict(zip(elements, ratio))

    print(run)
    mass = [masses[i]*ratios[i] for i in elements]
    mass = sum(mass)*param[run]['atoms']

    term = [i/mass for i in volume]

    fig, sub = pl.subplots(1, 1)
    xdata = list(runs[run]['c_mytemp'])
    sub.plot(xdata, term, 'b.', label='Data Points')

    # Find bottom percent of data to fit
    length = len(xdata)
    start0 = 0
    end0 = math.floor(0.1*length)

    x0 = xdata[start0:end0]
    y0 = term[start0:end0]
    fit0 = np.polyfit(x0, y0, 1)
    fitf0 = np.poly1d(fit0)
    yfit0 = fitf0(xdata)

    fitrange0 = str([math.floor(xdata[start0]), math.floor(xdata[end0])])
    sub.plot(xdata, yfit0, 'r', label='Fit Range of '+fitrange0+' [K]')

    # Find top percent of data to fit
    start1 = math.ceil(0.15*length)
    end1 = -1
    x1 = xdata[start1:end1]
    y1 = term[start1:end1]
    fit1 = np.polyfit(x1, y1, 1)
    fitf1 = np.poly1d(fit1)
    yfit1 = fitf1(xdata)

    fitrange1 = str([math.floor(xdata[start1]), math.floor(xdata[end1])])
    sub.plot(xdata, yfit1, 'c', label='Fit Range of '+fitrange1+' [K]')

    try:
        npoints = 2
        point = [0]*(npoints+1)  # A point larger than 1 to start with
        tolerance = abs(max(term)-min(term))  # The initial tolerance

        # Iterate until point of intersection is found between fits
        count = 0
        while len(point) > npoints:
            point = np.argwhere(np.isclose(yfit0, yfit1, atol=tolerance)).reshape(-1)
            tolerance -= tolerance/10

            if count > 100:
                break

            count += 1

        temps = np.array(xdata)[point]
        temp = math.floor(sum(temps)/len(temps))
        sub.axvline(x=temp, linestyle='--', label='Fit Intersection at '+str(temp)+' [K]')

    except Exception:
        pass

    sub.set_xlabel('Temperature [K]')
    sub.set_ylabel('Specific Volume [A^3/g]')
    sub.legend(loc='upper left')
    sub.grid()
    fig.savefig('../figures/volume_'+run)
