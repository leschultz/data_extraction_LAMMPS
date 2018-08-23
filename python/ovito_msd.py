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
    data pipeline. This loops over for all and each particle type.
    '''

    dispmag = input.particle_properties.displacement_magnitude.array

    # Grab the number of particle types
    types = []
    for type in input.particles['Particle Type'].types:
        types.append(type.id)

    for item in types:
        index = (input.particles['Particle Type'] == item)

        # Compute MSD for a type of atom
        msd = np.sum(dispmag[index] ** 2) / len(dispmag[index])

        # Output MSD value as a global attribute:
        attr_name = 'MSD_type'+str(item)
        output.attributes[attr_name] = msd

    # Compute MSD for all atoms
    msd = np.sum(dispmag ** 2) / len(dispmag)
    output.attributes['MSD'] = msd


# Load the data for trajectories
def msdcalc(name, start, stop):
    '''
    Load the lammps trajectories and calculate MSD.
    '''

    # The file extension
    extension = '.lammpstrj'

    # Load input data and create an ObjectNode with a data pipeline.
    node = import_file(data_directory+name+extension, multiple_frames=True)

    # Calculate per-particle displacements with respect to a start
    modifier = CalculateDisplacementsModifier()
    modifier.assume_unwrapped_coordinates = True
    modifier.reference.load(data_directory+name+extension)
    modifier.reference_frame = start
    node.modifiers.append(modifier)

    # Insert custom modifier into the data pipeline.
    node.modifiers.append(PythonScriptModifier(function=modify))

    # The variables where data will be held
    msd = []
    step = []
    msd_types = {}
    order = []
    for type in node.compute().particles['Particle Type'].types:
        msd_types[type.id] = []
        order.append(type.id)

    # Compute the MSD for each frame of interest
    for frame in range(start, stop+1):
        out = node.compute(frame)
        msd.append(out.attributes['MSD'])
        step.append(out.attributes['Timestep'])

        for type in out.particles['Particle Type'].types:
            attr_name = 'MSD_type'+str(type.id)
            msd_types[type.id].append(out.attributes[attr_name])

    # The output directory with the run name
    output = dump_directory+name+'_msd.txt'

    # Columns of data
    columns = [step, msd]

    # Create columns for each particle type and ensure type order
    order.sort()
    for item in order:
        columns.append(msd_types[item])

    # Save data with a step column and an MSD column
    np.savetxt(output, np.transpose(columns))
