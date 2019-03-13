from scipy.interpolate import UnivariateSpline as spline
from matplotlib import pyplot as pl

from scipy.signal import argrelextrema

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

    length = len(xdata)

    # Fit a spline and find the derivatives
    s = spline(
               x=xdata,
               y=ydata,
               k=5,
               )

    dds = s.derivative(2)  # Take a second derivative

    xnew = np.linspace(xdata[0], xdata[-1], 1000)  # Make smooth
    yspline = s(xnew)
    ddyspline = dds(xnew)

    maxsplineindex = argrelextrema(ddyspline, np.greater)[0][0]
    minsplineindex = argrelextrema(ddyspline, np.less)[0][0]

    if not maxsplineindex:
        maxsplineindex = 0

    if not minsplineindex:
        minsplineindex = 0

    if maxsplineindex < minsplineindex:
        splineindex = maxsplineindex
    else:
        splineindex = minsplineindex

    return xnew, yspline, ddyspline, splineindex


def plotknee(xdata, ydata, xfit, yfit, ddyfit, kneeindex, name):
    '''
    Plot data to visualize where the knee of a curve occurs.

    inputs:
        xdata = The x-axis data
        ydata = The y-axis data
        xfit = The x-axis data for the spline fit
        yfit = The y-axis data for the spline fit
        ddyfit = The y-axis data for the second derivative of yfit
        kneeindex = The index of the data of the knee
        name = The beginning save name for the plots

    outputs:
        saves plots in directory where it is run
    '''

    legenddigits = 6  # The display digit length for plots legends

    fig, ax = pl.subplots(2, 1)

    ax[0].set_title('Analysis of the rate of change of the slope')

    splineintersection = (
                          float(str(xfit[kneeindex])[:legenddigits]),
                          float(str(yfit[kneeindex])[:legenddigits])
                          )

    ax[0].plot(xdata, ydata, marker='.', label='Data')
    ax[0].plot(xfit, yfit, label='Spline Fit')
    ax[0].axvline(
                  x=xfit[kneeindex],
                  color='k',
                  label='Knee at '+str(splineintersection)
                  )
    ax[0].axhline(y=yfit[kneeindex], color='k')
    ax[0].set_ylabel('y data')
    ax[0].set_xlabel('x data')
    ax[0].legend()
    ax[0].grid()

    splineintersectionerr = (
                             float(str(xfit[kneeindex])[:legenddigits]),
                             float(str(ddyfit[kneeindex])[:legenddigits])
                             )

    ax[1].plot(xfit, ddyfit)
    ax[1].axvline(
                  x=xfit[kneeindex],
                  color='k',
                  label='Knee at '+str(splineintersectionerr)
                  )
    ax[1].axhline(y=ddyfit[kneeindex], color='k')
    ax[1].set_ylabel('Second derivative')
    ax[1].set_xlabel('x data')
    ax[1].legend()
    ax[1].grid()

    fig.tight_layout()
    fig.savefig(name+'_second_derivative_method')

    pl.close('all')
