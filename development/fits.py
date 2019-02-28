from scipy.interpolate import UnivariateSpline as spline
from scipy.stats import linregress as fit
from matplotlib import pyplot as pl

import numpy as np


def fitmethod(xdata, ydata):
    '''
    Determine error from fiting multiple lines on a set of data.
    Fit all the data and then remove lower temperatures and calculate
    the differences between the fitted y values and the actual y values
    normalized by the length of data used for fitting.

    inputs:
        xdata = The x-axis data
        ydata = The y-axis data
        name = the beginning save name for the plots

    outputs:
        toperrsnorm = The errors normalized by the maximum error
    '''

    length = len(xdata)

    toperrs = []
    for i in range(length-1):

        # Remove data from the beginning
        x = xdata[i:]
        y = ydata[i:]

        # The beginning and end points for the data of interest
        xpoints = [x[0], x[-1]]
        ypoints = [y[0], y[-1]]

        topfit = fit(xpoints, ypoints)

        slope = topfit[0]
        intercept = topfit[1]

        yfit = [i*slope+intercept for i in x]

        toperr = sum([abs(i-j) for i, j in zip(y, yfit)])/len(x)

        toperrs.append(toperr)

    toperrsnorm = np.array(toperrs)/max(toperrs)

    return toperrsnorm


def cutindex(toperrsnorm, cutoff):
    '''
    Define the cutoff index based on a fraction of the maximum normalized
    error.

    inputs:
       toperrsnorm = The normalized erros from fitmethod
        cutoff = The fraction cutoff 

    outputs:
        fitindex = The idnex where the cutoff criterion is met
    '''

    count = 0
    for i in toperrsnorm:
        if i > cutoff:
            count += 1

        else:
            fitindex = count-1
            break

    return fitindex


def knees(xdata, ydata, lines, name):
    '''
    Use several methods to find the knee given x and y data. Data
    has to be strictly increasing.

    inputs:
        xdata = The x-axis data
        ydata = The y-axis data
        name = The beginning save name for the plots

    outputs:
        kneeindex = The last index of method
        plot of method
    '''

    degree = 5  # The degree for the fitting spline
    length = len(xdata)

    # Determine the linear fitting range
    count = 0
    cutoff = 0.1
    indexes = [length-1]
    for i in range(lines):
        toperrsnorm = fitmethod(
                                xdata[:indexes[count]],
                                ydata[:indexes[count]]
                                )

        fitindex = cutindex(toperrsnorm, cutoff)
        indexes.append(fitindex)

        count += 1

    fig, ax = pl.subplots()

    ax.plot(xdata, ydata, marker='.', label='Data')
    for index in indexes:
        ax.plot(
                xdata[index],
                ydata[index],
                marker='o',
                color='r',
                )

    '''
    for i in range(len(indexes)-1):
        xpoints = (xdata[indexes[i]], xdata[indexes[i+1]])
        ypoints = (ydata[indexes[i]], ydata[indexes[i+1]])

        linefit = fit(xpoints, ypoints)
        slope = linefit[0]
        intercept = linefit[1]

        function = lambda x: slope*x+intercept
        yfit = function(xdata)

        ax.plot(
                xdata,
                yfit,
                linestyle='--',
                )

    '''
    ax.set_ylabel('y data')
    ax.set_xlabel('x data')
    ax.set_ylim([min(ydata), max(ydata)])
    ax.legend()
    ax.grid()

    fig.tight_layout()
    fig.savefig(name+'_fit')

    pl.close('all')

    kneeindex = indexes[-1]
    xkneeval = xdata[kneeindex]
    ykneeval = ydata[kneeindex]
    return kneeindex, xkneeval, ykneeval

kneesdata = []

# Evaluate a sigmoid function
s = '50/(1+np.exp(-x*2))'
s = 'lambda x: '+s
f = eval(s)
xdata = np.linspace(-3, 0)
ydata = f(xdata)

i = knees(xdata, ydata, 3, 'sigmoid1')
kneesdata.append(i)

# Evaluate a sigmoid function
s = '50/(1+np.exp(-x*2))'
s = 'lambda x: '+s
f = eval(s)
xdata = np.linspace(-3, 1)
ydata = f(xdata)

i = knees(xdata, ydata, 3, 'sigmoid2')
kneesdata.append(i)

# Evaluate a sigmoid function
s = '50/(1+np.exp(-x*2))'
s = 'lambda x: '+s
f = eval(s)
xdata = np.linspace(-3, 3)
ydata = f(xdata)

i = knees(xdata, ydata, 3, 'sigmoid3')
kneesdata.append(i)

fig, ax = pl.subplots()
ax.plot(xdata, ydata)
for item in kneesdata:
    ax.axvline(x=item[1])

