'''
Modified from https://ovito.org/manual/python/modules/ovito_modifiers.html
'''

from ovito.modifiers import CalculateDisplacementsModifier
from ovito.modifiers import PythonScriptModifier
from ovito.io import import_file

import numpy as np
import os

# List the directories used
first_directory = os.getcwd()
data_directory = first_directory + '/../data/lammpstrj/'
dump_directory = first_directory + '/../data/analysis/msd/'


# Define the custom modifier function:
def modify(frame, input, output):
    '''
    Access the per-particle displacement magnitudes computed by an existing
    Displacement Vectors modifier that precedes this custom modifier in the
    data pipeline:
    '''

    dispmag = input.particle_properties.displacement_magnitude.array

    # Compute MSD:
    msd = np.sum(dispmag ** 2) / len(dispmag)

    # Output MSD value as a global attribute:
    output.attributes["MSD"] = msd


# Load the data for trajectories
def msdcalc(name, start):
    '''
    Load the lammps trajectories and calculate MSD.
    '''

    # Change to data directory
    os.chdir(data_directory)

    # The file extension
    extension = '.lammpstrj'

    # Load input data and create an ObjectNode with a data pipeline.
    node = import_file(name+extension, multiple_frames=True)

    # Calculate per-particle displacements with respect to a start
    modifier = CalculateDisplacementsModifier()
    modifier.assume_unwrapped_coordinates = True
    modifier.reference.load(name+extension)
    modifier.reference_frame = start
    node.modifiers.append(modifier)

    # Insert custom modifier into the data pipeline.
    node.modifiers.append(PythonScriptModifier(function=modify))

    # Compute the msd for each frame of interest
    msd = []
    step = []
    for frame in range(start, node.source.num_frames):
        out = node.compute(frame)
        msd.append(out.attributes['MSD'])
        step.append(out.attributes['Timestep'])

    # Change to analysis directory
    os.chdir(dump_directory)

    # The output directory with the run name
    output = dump_directory+name+'_msd.txt'

    # Save data with a step column and an MSD column
    np.savetxt(output, np.c_[step, msd])

    # Change back to original directory
    os.chdir(first_directory)
