from matplotlib import pyplot as pl
from scipy import stats as st

from matplotlib import lines
from itertools import islice

from autocovariance import auto
from dfdiff import diffusionimport
from ukuiestimator import error as ukui
from batchmeans import error as batch

import pandas as pd
import numpy as np
import os


def percent(x, y):
    return [i/j*100.0 for i, j in zip(x, y)]


data = diffusionimport('../export/')
errors = {}
for folder in data:
    errors[folder] = []
    for temp in data[folder]['origins']:
        cols = list(data[folder]['origins'][temp].columns.values)[1:]
        cols = [i for i in cols if 'Err' not in i]

        regulardata = data[folder]['regular'][temp]
        modata = data[folder]['origins'][temp]

        k, r = auto(modata['all'])

        count = 0
        for i in r:
            if i >= 0.0:
                index = count
                count += 1
            else:
                break

        errordf = {}
        for col in cols:
            errordf[col+'_diff'] = regulardata[col]
            errordf[col+'_fiterr'] = regulardata[col+'_Err']
            errordf[col+'_mo_ukui'] = ukui(list(modata[col]))
            errordf[col+'_mo_batch(a=5)'] = batch(list(modata[col]), a=5)
            errordf[col+'_mo_batch(a=10)'] = batch(list(modata[col]), a=10)
            errordf[col+'_mo_batch(b=lcorr)'] = batch(list(modata[col]), b=k[index])
            errordf[col+'_mo_scipysem'] = st.sem(list(modata[col]))
            errordf[col+'_mo_fitavg'] = np.mean(list(modata[col+'_Err']))

        errordf['temp'] = temp
        errordf = pd.DataFrame(errordf, index=[0])
        errors[folder].append(errordf)

for folder in data:
    errors[folder] = pd.concat(errors[folder])

batch5label = lines.Line2D(
                           [],
                           [],
                           color='b',
                           marker='.',
                           linestyle='None',
                           markersize=8,
                           label='Batch Means (a=5)'
                           )

batch10label = lines.Line2D(
                            [],
                            [],
                            color='r',
                            marker='.',
                            linestyle='None',
                            markersize=8,
                            label='Batch Means (a=10)'
                            )

batchlcorrlabel = lines.Line2D(
                               [],
                               [],
                               color='g',
                               marker='.',
                               linestyle='None',
                               markersize=8,
                               label='Batch Means (b=lcorr)'
                               )

ukuilabel = lines.Line2D(
                         [],
                         [],
                         color='y',
                         marker='+',
                         linestyle='None',
                         markersize=8,
                         label='Ukui Estimator'
                         )

scipylabel = lines.Line2D(
                          [],
                          [],
                          color='k',
                          marker='x',
                          linestyle='None',
                          markersize=8,
                          label='Scipy SEM'
                          )

fitlabel = lines.Line2D(
                        [],
                        [],
                        color='g',
                        marker='^',
                        linestyle='None',
                        markersize=8,
                        label='Fitting Error Averaged'
                        )

plotlabels = []
plotlabels.append(batch5label)
plotlabels.append(batch10label)
plotlabels.append(batchlcorrlabel)
plotlabels.append(ukuilabel)
plotlabels.append(scipylabel)
plotlabels.append(batchlcorrlabel)

for folder in errors:

    cols = list(errors[folder].columns.values)
    try:
        elements = [i.split('_')[0] for i in cols if len(i.split('_')) > 1]

    except Exception:
        pass

    elements = list(set(elements))

    for el in elements:
        fig, ax = pl.subplots(2, 2, figsize=(10, 10))

        x = errors[folder]['temp']

        ax[0][0].plot(x, errors[folder][el+'_diff'], 'b.')

        ax[0][0].set_ylabel('Diffusion [*10^-4 cm^2 s^-1]')
        ax[0][0].set_xlabel('Temperature [K]')
        ax[0][0].grid()

        ax[0][1].plot(x, errors[folder][el+'_fiterr'], 'r.')

        ax[0][1].set_ylabel('Diffusion Fit Error [*10^-4 cm^2 s^-1]')
        ax[0][1].set_xlabel('Temperature [K]')
        ax[0][1].grid()

        ax[1][0].plot(x, errors[folder][el+'_mo_batch(a=5)'], 'b.')
        ax[1][0].plot(x, errors[folder][el+'_mo_batch(a=10)'], 'r.')
        ax[1][0].plot(x, errors[folder][el+'_mo_batch(b=lcorr)'], 'g.')
        ax[1][0].plot(x, errors[folder][el+'_mo_ukui'], 'y+')
        ax[1][0].plot(x, errors[folder][el+'_mo_scipysem'], 'kx')
        ax[1][0].plot(x, errors[folder][el+'_mo_fitavg'], 'g^')

        ax[1][0].set_ylabel('Diffusion MO Error [*10^-4 cm^2 s^-1]')
        ax[1][0].set_xlabel('Temperature [K]')
        ax[1][0].legend(handles=plotlabels, loc='best')
        ax[1][0].grid()

        # Change values to percent error
        diff = errors[folder][el+'_diff']
        runsbatch5percent = percent(errors[folder][el+'_mo_batch(a=5)'], diff)
        runsbatch10percent = percent(errors[folder][el+'_mo_batch(a=10)'], diff)
        runsbatchlcorrpercent = percent(errors[folder][el+'_mo_batch(b=lcorr)'], diff)
        runsukuipercent = percent(errors[folder][el+'_mo_ukui'], diff)
        runsscipypercent = percent(errors[folder][el+'_mo_scipysem'], diff)
        fiterrorpercent = percent(errors[folder][el+'_mo_fitavg'], diff)

        ax[1][1].plot(x, runsbatch5percent, 'b.')
        ax[1][1].plot(x, runsbatch10percent, 'r.')
        ax[1][1].plot(x, runsbatchlcorrpercent, 'g.')
        ax[1][1].plot(x, runsukuipercent, 'y+')
        ax[1][1].plot(x, runsscipypercent, 'kx')
        ax[1][1].plot(x, fiterrorpercent, 'g^')

        ax[1][1].set_ylabel('Diffusion MO Percent Error')
        ax[1][1].set_xlabel('Temperature [K]')
        ax[1][1].legend(handles=plotlabels, loc='best')
        ax[1][1].grid()

        name = folder+'_element_'+el
        fig.tight_layout()
        fig.savefig('../'+name)
        pl.close(fig)
