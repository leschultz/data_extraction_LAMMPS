'''
Modified from https://ovito.org/manual/python/modules/ovito_modifiers.html
'''

from ovito.modifiers import CalculateDisplacementsModifier
from ovito.modifiers import CoordinationNumberModifier
from ovito.modifiers import VoronoiAnalysisModifier
from ovito.modifiers import PythonScriptModifier
from ovito.io import import_file
from scipy import stats as st

import numpy as np
import os


# Define the custom modifier function:
def msdmodify(frame, input, output):
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
        msd = np.sum(dispmag[index]**2)/len(dispmag[index])
        msdeim = st.sem(dispmag[index]**2)

        # Output MSD value as a global attribute:
        attr_name = 'MSD_type'+str(item)
        output.attributes[attr_name] = msd
        attr_name_EIM = 'MSD_type_EIM'+str(item)
        output.attributes[attr_name_EIM] = msdeim

    # Compute MSD for all atoms
    msd = np.sum(dispmag**2)/len(dispmag)
    msdeim = st.sem(dispmag**2)
    output.attributes['MSD'] = msd
    output.attributes['MSD_EIM'] = msdeim


# Load the data for trajectories
def calc(name, start, stop):
    '''
    Load the lammps trajectories and calculate MSD.
    '''

    # Load input data and create an ObjectNode with a data pipeline.
    node = import_file(name, multiple_frames=True)

    # Calculate per-particle displacements with respect to a start
    modifier = CalculateDisplacementsModifier()
    modifier.assume_unwrapped_coordinates = True
    modifier.reference.load(name)
    modifier.reference_frame = start
    node.modifiers.append(modifier)

    # Insert custom modifier into the data pipeline.
    node.modifiers.append(PythonScriptModifier(function=msdmodify))

    # The variables where data will be held
    msd = []
    msdeim = []
    step = []
    msd_types = {}
    msd_types_eim = {}
    order = []
    for type in node.compute().particles['Particle Type'].types:
        msd_types[type.id] = []
        msd_types_eim[type.id] = []
        order.append(type.id)

    # Compute the MSD for each frame of interest
    for frame in range(start, stop+1):
        out = node.compute(frame)
        msd.append(out.attributes['MSD'])
        msdeim.append(out.attributes['MSD_EIM'])
        step.append(out.attributes['Timestep'])

        for type in out.particles['Particle Type'].types:
            attr_name = 'MSD_type'+str(type.id)
            attr_name_eim = 'MSD_type_EIM'+str(type.id)
            msd_types[type.id].append(out.attributes[attr_name])
            msd_types_eim[type.id].append(out.attributes[attr_name_eim])

    # MSD data
    msdall = {}
    msdall['all'] = msd
    msdall['all_EIM'] = msdeim

    # Create columns for each particle type and ensure type order
    for key in msd_types:
        msdall[str(key)] = msd_types[key]
        msdall[str(key)+'_EIM'] = msd_types_eim[key]

    return msdall


def rdfcalc(name, frame, cut, bins):
    '''
    Use ovito to calculate RDF
    '''

    # Load a particle dataset
    node = import_file(name, multiple_frames=True)

    # Apply modifier
    modifier = CoordinationNumberModifier(cutoff=cut, number_of_bins=bins)
    node.modifiers.append(modifier)

    # Compute RDF of the current frame
    out = node.compute(frame)

    return modifier.rdf


def vp(name, frame, maxedge=6, threshold=0.1):
    '''
    Calculate the Voronoi polyhedra.

    inputs:
            name = trajectory file
            frame = frame of interest
            maxedge = the maximum Voronoi polyhedra edge count
            threshold = minimum length for an edge to be counted
    '''

    # Load input data and create an ObjectNode with a data pipeline.
    node = import_file(name, multiple_frames=True)

    voro = VoronoiAnalysisModifier(
                                   compute_indices=True,
                                   use_radii=False,
                                   edge_count=maxedge,
                                   edge_threshold=threshold
                                   )

    node.modifiers.append(voro)
    out = node.compute(frame)

    indexes = out.particle_properties['Voronoi Index'].array

    return indexes
