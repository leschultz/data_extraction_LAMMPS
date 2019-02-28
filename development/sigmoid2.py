from scipy.interpolate import UnivariateSpline as spline
from scipy.stats import linregress as fit
from matplotlib import pyplot as pl

import numpy as np


def sigmoid(x):
    return 50/(1+np.exp(-x*2))

xdata = np.linspace(-3, 0)
ydata = sigmoid(xdata)

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

ax[0].plot(xdata, ydata, marker='.', label='Data')
ax[0].axvline(x=xdata[fitindex], color='k', label='Knee at '+str((xdata[fitindex], ydata[fitindex])))
ax[0].set_ylabel('50/(1+exp(-x*2))')
ax[0].set_xlabel('x values')
ax[0].legend()
ax[0].grid()


ax[1].plot(toperrsnorm)
ax[1].axvline(x=fitindex, color='k', label='Knee at '+str((fitindex, cutoff)))
ax[1].axhline(y=cutoff, color='k')
ax[1].set_ylabel('Error normalized by maximum error')
ax[1].set_xlabel('Index')
ax[1].legend()
ax[1].grid()

fig.tight_layout()
fig.savefig('sigmoid_fit_2')

'''
Find the knee based on how a second derivative behaves.
'''

# Fit a spline and find the derivatives
degree = 5
s = spline(xdata, ydata, k=degree)
ds = s.derivative()
dds = s.derivative(2)

yspline = s(xdata)
dyspline = ds(xdata)
ddyspline = dds(xdata)

splineindex = np.argmax(ddyspline)

fig, ax = pl.subplots(2, 1)

ax[0].set_title('Analysis of the rate of change of the slope')

ax[0].plot(xdata, ydata, marker='.', label='Data')
ax[0].plot(xdata, yspline, label='Spline Fit')
ax[0].axvline(x=xdata[splineindex], color='k', label='Knee at '+str((xdata[splineindex], yspline[splineindex])))
ax[0].set_ylabel('50/(1+exp(-x*2))')
ax[0].set_xlabel('x values')
ax[0].legend()
ax[0].grid()


ax[1].plot(xdata, ddyspline)
ax[1].axvline(x=xdata[splineindex], color='k', label='Knee at '+str((xdata[splineindex], ddyspline[splineindex])))
ax[1].axhline(y=ddyspline[splineindex], color='k')
ax[1].set_ylabel('Second derivative')
ax[1].set_xlabel('x values')
ax[1].legend()
ax[1].grid()

fig.tight_layout()
fig.savefig('sigmoid_derivative_2')
