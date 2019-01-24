from PyQt5 import QtGui  # Added to be able to import ovito

import pandas as pd
import numpy as np

from physical.ovito_calc import vp


def icofrac(name, frame, *args, **kwargs):
    '''
    Compute the fraction of ICO clusters.

    inputs:
            name = trajectory file name
            frame = frame of interest

    outputs:
            df = fraction of VP for harcoded indexes
    '''

    # The VP for a frame
    indexes = vp(name, frame, *args, **kwargs)

    size = indexes.shape
    zeros = np.zeros(size[1], dtype=int)

    # (0, 0, 0, 0, 12, ...) rest are zero
    ico1 = zeros.copy()
    ico1[4] = 12

    # (0, 0, 0, 1, 10, 2, ...) rest are zero
    ico2 = zeros.copy()
    ico2[3] = 1
    ico2[4] = 10
    ico2[5] = 2

    # (0, 0, 0, 1, 9, 3, ...) rest are zero
    ico3 = zeros.copy()
    ico3[3] = 1
    ico3[4] = 9
    ico3[5] = 3

    # Store clusters of interest
    clusters = {
                '(0, 0, 0, 0, 12)': ico1,
                '(0, 0, 0, 1, 10, 2)': ico2,
                '(0, 0, 0, 1, 9, 3)': ico3,
                }

    # Excat matches for clusters
    strictcounts = {
                    '(0, 0, 0, 0, 12)': 0,
                    '(0, 0, 0, 1, 10, 2)': 0,
                    '(0, 0, 0, 1, 9, 3)': 0,
                    }

    # n_5 >= 10
    geico1 = (4, 10)

    # n_5 >= 8
    geico2 = (4, 8)

    geclusters = {
                  'n_5 >= 10': geico1,
                  'n_5 >= 8': geico2,
                  }

    # Grater than or equal for an index
    gecounts = {
                'n_5 >= 10': 0,
                'n_5 >= 8': 0,
                }

    # Find exact match count for VP
    for i in indexes:

        # Counts for exact matches
        for key in clusters:
            if np.array_equal(clusters[key], i):
                strictcounts[key] += 1

        # Greater than or equal matches for an index
        for key in geclusters:
            if i[geclusters[key][0]] >= geclusters[key][1]:
                gecounts[key] += 1

    # Calculate VP fraction
    strictcountsfrac = {}
    for key in strictcounts:
        strictcountsfrac[key] = strictcounts[key]/size[0]

    gecountsfrac = {}
    for key in gecounts:
        gecountsfrac[key] = gecounts[key]/size[0]

    strictdf = pd.DataFrame(strictcountsfrac, index=['fraction'])
    gedf = pd.DataFrame(gecountsfrac, index=['fraction'])

    dframes = [strictdf, gedf]
    df = pd.concat(dframes, sort=False)
    df = df.groupby(level=0).sum()

    return df


def sindex(x, percent):
    '''
    Find the indexes on the ends and middle of an s-curve given a percent
    deviation. The percent deviation is the last value from each end where
    the value exceds a percent differnce. This function assumes the data
    increases as a function of time.

    inputs:
        x = data for the s-curve
        percent = The percent deviation from end values

    outputs:
        indexes = the indexes from the ends and middle of the s-curve
        lindex = the leftmost index after percent comparison
        mindex = an index in the middle
        rindex = the rightmost index after percent comparison
    '''

    try:
        percent /= 100.0  # Decimal form

        high = max(x)
        endslice = len(x)-1

        minpercent = high*percent  # Min bound for comparison

        count = 0
        lval = x[0]  # The leftmost value
        while lval <= minpercent:
            lval = x[count]
            count += 1

        if count != 0:
            lindex = count-1  # Subtract because of the final count addition
        else:
            lindex = 0

        minpercent = high*(1-percent)  # Min bound for comparison

        count = endslice
        rval = x[-1]  # The rightmost value
        while rval >= minpercent:
            rval = x[count]
            count -= 1

        if count != endslice:
            rindex = count+1  # Add because of the final count subtraction

        else:
            rindex = endslice

        mindex = lindex+(rindex-lindex)//2  # Get the middle index

    except Exception:
        print('Sigmoid curve not sufficiently smooth or ill defined percent.')
        print('Setting indexes to 0.')
        lindex = 0
        mindex = 0
        rindex = 0

    return lindex, mindex, rindex
