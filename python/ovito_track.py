'''
Modified from https://ovito.org/manual/python/modules/ovito_modifiers.html
'''

from ovito.modifiers import CoordinationNumberModifier
from ovito.modifiers import PythonScriptModifier
from ovito.io import import_file

import numpy as np
import ast
import os

# List the directories used
first_directory = os.getcwd()
data_directory = first_directory + '/../data/lammpstrj/'
dump_directory = first_directory + '/../data/analysis/coordination/'


def coordinated_particles(frame, input, output):
    '''
    Get the coordination numbers for each particle
    '''

    particle_id = input.particle_properties['Particle Identifier']
    particle_type = input.particle_properties['Particle Type']
    coord_number = input.particle_properties['Coordination']

    output.attributes['id'] = list(particle_id)
    output.attributes['type'] = list(particle_type)
    output.attributes['coord'] = list(coord_number)


def rdfcalc(name, start, stop, cut):
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
    modifier = CoordinationNumberModifier(cutoff=cut)
    node.modifiers.append(modifier)

    # Insert custom modifier into the data pipeline.
    modifier = PythonScriptModifier(function=coordinated_particles)
    node.modifiers.append(modifier)

    # Grab the atom types
    out = node.compute(start)
    atomtype = np.array(ast.literal_eval(out.attributes['type']))
    atomtypes = list(set(atomtype))

    # Create variable to store coordination numbers
    coord_numbers = {}
    for item in atomtypes:
        coord_numbers[item] = []

    steps = []
    for frame in range(start, stop+1):

        # Compute RDF of the current frame
        out = node.compute(frame)

        # Grab the time step
        step = out.attributes['Timestep']
        steps.append(step)

        # Turn the stupid string output into a list
        atom = np.array(ast.literal_eval(out.attributes['id']))
        atomtype = np.array(ast.literal_eval(out.attributes['type']))
        atomcoord = np.array(ast.literal_eval(out.attributes['coord']))

        for item in atomtypes:
            index = atomtype == item

            # Return a list of coordination number for element type
            atoms_filtered = list(atomcoord[index])
            coord_numbers[item].append(atoms_filtered)

    print(coord_numbers[1][0].count(6, 7))

    # Go back to original directory
    os.chdir(first_directory)
