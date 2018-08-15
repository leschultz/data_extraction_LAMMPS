from ovito.modifiers import CalculateDisplacementsModifier
from ovito.modifiers import PythonScriptModifier
from ovito.io import import_file, export_file

import numpy
import os

# List the directories used
first_directory = os.getcwd()
data_directory = first_directory + '/../data/lammpstrj'
dump_directory = first_directory + '/../data/analysis'


# Define the custom modifier function:
def modify(frame, input, output):
    '''
    Access the per-particle displacement magnitudes computed by an existing
    Displacement Vectors modifier that precedes this custom modifier in the
    data pipeline:
    '''

    displacement_magnitudes = input.particle_properties.displacement_magnitude.array

    # Compute MSD:
    msd = numpy.sum(displacement_magnitudes ** 2) / len(displacement_magnitudes)

    # Output MSD value as a global attribute:
    output.attributes["MSD"] = msd


# Load the data for trajectories
def loadtrj(name):
    '''
    Load the lammps trajectories.
    '''

    # Change to data directory
    os.chdir(data_directory)

    # The file extension
    extension = '.lammpstrj'

    # Load input data and create an ObjectNode with a data pipeline.
    node = import_file(name+extension, multiple_frames=True)

    # Calculate per-particle displacements with respect to initial simulation frame
    dmod = CalculateDisplacementsModifier()
    dmod.assume_unwrapped_coordinates = True
    dmod.reference.load(name+extension)
    node.modifiers.append(dmod)

    # Change back to original directory
    os.chdir(first_directory)

    return node


def msdcalc(name):
    '''
    Calculate the MSD for the loaded file
    '''

    node = loadtrj(name)

    # Insert custom modifier into the data pipeline.
    node.modifiers.append(PythonScriptModifier(function=modify))

    # Export calculated MSD value to txt:
    export_file(
                node,
                '../data/analysis/'+name+'_msd.txt',
                format='txt',
                columns=['Timestep', 'MSD'],
                multiple_frames=True
                )


def plotmsd(name):
    '''
    Plot the MSD data.
    '''

    # Change directory to file export directory
    os.chdir(dump_directory)

    # File extension for import
    extension = '_msd.txt'

    step = []
    msd = []
    with open(name+extension) as inputfile:
        iterlines = iter(inputfile)
        next(iterlines)
        for line in iterlines:
            value = line.strip().split(' ')
            step.append(value[0])
            msd.append(value[1])

    print(msd)

    # Change back to the first directory
    os.chdir(first_directory)

