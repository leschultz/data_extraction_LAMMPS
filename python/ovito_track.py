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


def rdfcalc(name, frame, cut, coordination):
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

    # Compute RDF of the current frame
    out = node.compute(frame)

    # Turn the stupid string output into a list
    atom = np.array(ast.literal_eval(out.attributes['id']))
    atomtype = np.array(ast.literal_eval(out.attributes['type']))
    atomcoord = np.array(ast.literal_eval(out.attributes['coord']))

    # Return a list of atoms with a coordination number
    atoms_filtered = list(atom[atomcoord == coordination])

    print(atoms_filtered)

    # Accumulate RDF histograms
    step = out.attributes['Timestep']

    # The ouput directory with the run name
    output = dump_directory+name+'_step'+str(step)+'_coord.txt'

    # Go back to original directory
    os.chdir(first_directory)
