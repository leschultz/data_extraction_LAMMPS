from scipy.interpolate import InterpolatedUnivariateSpline as spline
from scipy.signal import argrelextrema
from scipy.stats import linregress as fit
from matplotlib import pyplot as pl

import numpy as np


def knees(xdata, ydata):
    '''
    Find the knee based on how a second derivative behaves.
    Data has to be strictly increasing.

    inputs:
        xdata = The x-axis data
        ydata = The y-axis data

    outputs:
        yspline = The y-valeus for fitted data
        ddyspline = The second derivative for fitted data
        splineindex = The index where the knee should occur
    '''

    degree = 5  # The degree for the fitting spline
    length = len(xdata)

    # Fit a spline and find the derivatives
    s = spline(xdata, ydata, k=degree)
    ds = s.derivative()
    dds = s.derivative(2)

    yspline = s(xdata)
    dyspline = ds(xdata)
    ddyspline = dds(xdata)

    splineindex = argrelextrema(ddyspline, np.greater)[0][0]

    return yspline, ddyspline, splineindex


def plotknee(xdata, ydata, yfit, ddyfit, kneeindex, name):
    '''
    Plot data to visualize where the knee of a curve occurs.

    inputs:
        xdata = The x-axis data
        ydata = The y-axis data
        name = The beginning save name for the plots

    outputs:
        saves plots in directory where it is run
    '''

    legenddigits = 6  # The display digit length for plots legends

    fig, ax = pl.subplots(2, 1)

    ax[0].set_title('Analysis of the rate of change of the slope')

    splineintersection = (
                          float(str(xdata[kneeindex])[:legenddigits]),
                          float(str(yfit[kneeindex])[:legenddigits])
                          )

    ax[0].plot(xdata, ydata, marker='.', label='Data')
    ax[0].plot(xdata, yfit, label='Spline Fit')
    ax[0].axvline(
                  x=xdata[kneeindex],
                  color='k',
                  label='Knee at '+str(splineintersection)
                  )
    ax[0].axhline(y=yfit[kneeindex], color='k')
    ax[0].set_ylabel('y data')
    ax[0].set_xlabel('x data')
    ax[0].legend()
    ax[0].grid()

    splineintersectionerr = (
                             float(str(xdata[kneeindex])[:legenddigits]),
                             float(str(ddyfit[kneeindex])[:legenddigits])
                             )

    ax[1].plot(xdata, ddyfit)
    ax[1].axvline(
                  x=xdata[kneeindex],
                  color='k',
                  label='Knee at '+str(splineintersectionerr)
                  )
    ax[1].axhline(y=ddyfit[kneeindex], color='k')
    ax[1].set_ylabel('Second derivative')
    ax[1].set_xlabel('x data')
    ax[1].legend()
    ax[1].grid()

    fig.tight_layout()
    fig.savefig(name+'_derivative')

    pl.close('all')


# Evaluate a sigmoid function
s = '50/(1+np.exp(-x*2))'
s = 'lambda x: '+s
f = eval(s)
xdata = np.linspace(-3, 0)
ydata = f(xdata)

yfit, ddyfit, kneeindex = knees(xdata, ydata)
plotknee(xdata, ydata, yfit, ddyfit, kneeindex, 'sigmoid1')

# Evaluate a sigmoid function
s = '50/(1+np.exp(-x*2))'
s = 'lambda x: '+s
f = eval(s)
xdata = np.linspace(-3, 1)
ydata = f(xdata)

yfit, ddyfit, kneeindex = knees(xdata, ydata)
plotknee(xdata, ydata, yfit, ddyfit, kneeindex, 'sigmoid2')

# Evaluate a sigmoid function
s = '50/(1+np.exp(-x*2))'
s = 'lambda x: '+s
f = eval(s)
xdata = np.linspace(-3, 3)
ydata = f(xdata)

yfit, ddyfit, kneeindex = knees(xdata, ydata)
plotknee(xdata, ydata, yfit, ddyfit, kneeindex, 'sigmoid3')
