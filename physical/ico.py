from PyQt5 import QtGui  # Added to be able to import ovito

from physical.ovito_calc import vp

import pandas as pd
import numpy as np

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
