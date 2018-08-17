'''
Modified from https://ovito.org/manual/python/modules/ovito_modifiers.html
'''

from ovito.modifiers import CoordinationNumberModifier
from ovito.io import import_file

import numpy as np
import os

# List the directories used
first_directory = os.getcwd()
data_directory = first_directory + '/../data/lammpstrj/'
dump_directory = first_directory + '/../data/analysis/'


def rdfcalc(name, frame, cut, bins):
    '''
    Use ovito to calculate RDF
    '''

    # Change directory to data location
    os.chdir(data_directory)

    # The file extension
    name = name + '.lammpstrj'

    # Load a particle dataset
    node = import_file(name, multiple_frames=True)

    # Apply modifier
    modifier = CoordinationNumberModifier(cutoff = cut, number_of_bins = bins)
    node.modifiers.append(modifier)

    # Initialize array for accumulated RDF historgram to zero
    total_rdf = np.zeros((modifier.number_of_bins, 2))

    # Compute RDF of the ucrrent frame
    node.compute(frame)

    # Accumulate RDF histograms
    total_rdf += modifier.rdf

    # The ouput directory with the run name
    output = dump_directory + name.split('.')[0] + str(frame) + 'frame_rdf.txt'

    # Export the computed RDF data to a text file.
    np.savetxt(output, total_rdf)

    # Go back to original directory
    os.chdir(first_directory)
