from scipy.interpolate import UnivariateSpline as spline
from scipy.stats import linregress as fit
from matplotlib import pyplot as pl

import numpy as np

def knees(xdata, ydata, name):
    '''
    Use several methods to find the knee given x and y data. Data
    has to be strictly increasing.

    inputs:
        xdata = The x-axis data
        ydata = The y-axis data
        name = the beginning save name for the plots

    outputs:
        plots
    '''

    degree = 5  # The degree for the fitting spline
    legenddigits = 4  # The display digit length for plots legends
    length = len(xdata)

    '''
    Fit all the data and then remove lower temperatures and calculate
    the differences between the fitted y values and the actual y values
    normalized by the length of data used for fitting.
    '''
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

    cutoff = 0.1
    count = 0
    for i in toperrsnorm:
        if i > cutoff:
            count += 1

        else:
            fitindex = count-1
            break

    fig, ax = pl.subplots(2, 1)

    ax[0].set_title('Minimization of error from multiple fits')

    fitintersection = (
                       float(str(xdata[fitindex])[:legenddigits]),
                       float(str(ydata[fitindex])[:legenddigits])
                       )
    ax[0].plot(xdata, ydata, marker='.', label='Data')
    ax[0].axvline(
                  x=xdata[fitindex],
                  color='k',
                  label='Knee at '+str(fitintersection)
                  )
    ax[0].axhline(y=ydata[fitindex], color='k')
    ax[0].set_ylabel('y data')
    ax[0].set_xlabel('x data')
    ax[0].legend()
    ax[0].grid()

    fitintersectionerr = (
                          float(str(fitindex)[:legenddigits]),
                          float(str(cutoff)[:legenddigits])
                          )
    ax[1].plot(toperrsnorm)
    ax[1].axvline(
                  x=fitindex,
                  color='k',
                  label='Knee at '+str(fitintersectionerr)
                  )
    ax[1].axhline(y=cutoff, color='k')
    ax[1].set_ylabel('Error normalized by maximum error')
    ax[1].set_xlabel('Index')
    ax[1].legend()
    ax[1].grid()

    fig.tight_layout()
    fig.savefig(name+'_fit')

    '''
    Find the knee based on how a second derivative behaves.
    '''

    # Fit a spline and find the derivatives
    s = spline(xdata, ydata, k=degree)
    ds = s.derivative()
    dds = s.derivative(2)

    yspline = s(xdata)
    dyspline = ds(xdata)
    ddyspline = dds(xdata)

    splineindex = np.argmax(ddyspline)

    fig, ax = pl.subplots(2, 1)

    ax[0].set_title('Analysis of the rate of change of the slope')

    splineintersection = (
                          float(str(xdata[splineindex])[:legenddigits]),
                          float(str(yspline[splineindex])[:legenddigits])
                          )

    ax[0].plot(xdata, ydata, marker='.', label='Data')
    ax[0].plot(xdata, yspline, label='Spline Fit')
    ax[0].axvline(
                  x=xdata[splineindex],
                  color='k',
                  label='Knee at '+str(splineintersection)
                  )
    ax[0].axhline(y=yspline[splineindex], color='k')
    ax[0].set_ylabel('y data')
    ax[0].set_xlabel('x data')
    ax[0].legend()
    ax[0].grid()

    splineintersectionerr = (
                             float(str(xdata[splineindex])[:legenddigits]),
                             float(str(ddyspline[splineindex])[:legenddigits])
                             )

    ax[1].plot(xdata, ddyspline)
    ax[1].axvline(
                  x=xdata[splineindex],
                  color='k',
                  label='Knee at '+str(splineintersectionerr)
                  )
    ax[1].axhline(y=ddyspline[splineindex], color='k')
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

knees(xdata, ydata, 'sigmoid1')

# Evaluate a sigmoid function
s = '50/(1+np.exp(-x*2))'
s = 'lambda x: '+s
f = eval(s)
xdata = np.linspace(-3, 1)
ydata = f(xdata)

knees(xdata, ydata, 'sigmoid2')

# Evaluate a sigmoid function
s = '50/(1+np.exp(-x*2))'
s = 'lambda x: '+s
f = eval(s)
xdata = np.linspace(-3, 3)
ydata = f(xdata)

knees(xdata, ydata, 'sigmoid3')
