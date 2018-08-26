'''
Modified from https://ovito.org/manual/python/modules/ovito_modifiers.html
'''

from ovito.modifiers import CoordinationNumberModifier
from ovito.io import import_file

import numpy as np
import os


def rdfcalc(name, frame, cut, bins):
    '''
    Use ovito to calculate RDF
    '''

    # Load a particle dataset
    node = import_file(name, multiple_frames=True)

    # Apply modifier
    modifier = CoordinationNumberModifier(cutoff=cut, number_of_bins=bins)
    node.modifiers.append(modifier)

    # Initialize array for accumulated RDF historgram to zero
    total_rdf = np.zeros((modifier.number_of_bins, 2))

    # Compute RDF of the current frame
    out = node.compute(frame)

    # Accumulate RDF histograms
    rdf = np.transpose(modifier.rdf)

    return rdf
