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
dump_directory = first_directory + '/../data/analysis/rdf/'


def rdfcalc(name, frame, cut, bins=100):
    '''
    Use ovito to calculate RDF
    '''

    # Change directory to data location
    os.chdir(data_directory)

    # The file extension
    extension = '.lammpstrj'

    # Load a particle dataset
    node = import_file(name+extension, multiple_frames=True)

    # Apply modifier
    modifier = CoordinationNumberModifier(cutoff=cut, number_of_bins=bins)
    node.modifiers.append(modifier)

    # Initialize array for accumulated RDF historgram to zero
    total_rdf = np.zeros((modifier.number_of_bins, 2))

    # Compute RDF of the ucrrent frame
    out = node.compute(frame)

    # Accumulate RDF histograms
    rdf = modifier.rdf
    step = out.attributes['Timestep']

    # The ouput directory with the run name
    output = dump_directory+name+'_step'+str(step)+'_rdf.txt'

    # Export the computed RDF data to a text file.
    np.savetxt(output, rdf)

    # Go back to original directory
    os.chdir(first_directory)
