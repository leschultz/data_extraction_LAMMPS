from analysis import load_lammpstrj
from matplotlib import pyplot as pl
from math import pi

import os


def wrap(names, calculation_step, number_of_atoms, columns, dimensions):
    '''
    This function gathers the coordinates of atoms and wraps them back into the
    original simulations box.
    '''

    # Where the data will be stored
    data_wrap = {}

    # The distances of each atom from the center of the simulation box
    distance = {}

    for item1 in names:
        # Load the data from a specific step
        data = load_lammpstrj(
                              item1,
                              calculation_step,
                              number_of_atoms,
                              columns
                              )

        for key in dimensions:

            # Check if atom is within a box
            count = 0
            for item2 in data[key]:

                # If outside negatively, then add box dimension until positive
                if data[key][count] < 0:
                    while data[key][count] < 0:
                        data[key][count] = (
                                            data[key][count] +
                                            dimensions[key]
                                            )

                # If outside positively, then subract box dimension until less
                # than the box dimension
                elif data[key][count] > dimensions[key]:
                    while data[key][count] > dimensions[key]:
                        data[key][count] = (
                                            data[key][count] -
                                            dimensions[key]
                                            )

                # Save data point if already within box
                else:
                    data[key][count] =  data[key][count]

                count += 1

        # Save the data for each run
        data_wrap[item1] = data

        # Gather the sitance from the center of the box for each atom
        distance[item1] = (
                           (data_wrap[item1]['x']-dimensions['x']/2.0)**2.0 +
                           (data_wrap[item1]['y']-dimensions['y']/2.0)**2.0 +
                           (data_wrap[item1]['z']-dimensions['z']/2.0)**2.0
                           )**0.5

    return data_wrap, distance


def radial_distribution(point, samples):
    '''
    This function analizes the radial distribution function. This function is
    also known as the pair correlation function. This function works by
    counting the number of atoms at different places in 3D space.
    '''

    # Get directories
    first_directory = os.getcwd()  # Python scripts
    lammpstrj_directory = first_directory+'/../data/lammpstrj/'  # Trajectory

    # List the names of files in the lammpstrj directory
    lammpstrj_file_names = os.listdir(lammpstrj_directory)

    # Gather the run name
    names = []
    for item in lammpstrj_file_names:
        names.append(item.split('_rate.lammpstrj')[0])

    # The columns of data to be inported
    columns = ([
                'id',
                'type',
                'x',
                'y',
                'z',
                'junk'
                ])

    # Grab the number of items from a file (NOTE: if runs have different number
    # of atoms then this will break)
    number_of_atoms = load_lammpstrj(names[0], 3, 1, None)
    number_of_atoms = number_of_atoms[0][0]

    # Grab the dimensions of the box from a file
    dimensions = {}
    dimensions['x'] = (load_lammpstrj(names[0], 5, 1, None))[1][0]
    dimensions['y'] = (load_lammpstrj(names[0], 6, 1, None))[1][0]
    dimensions['z'] = (load_lammpstrj(names[0], 7, 1, None))[1][0]

    # The step at wich calculations are done
    calculation_step = point*(number_of_atoms+9)+9

    # Wrap atom coordinates to appear within the original box and get distances
    data, distance = wrap(
                          names,
                          calculation_step,
                          number_of_atoms,
                          columns,
                          dimensions
                          )

    # The furthest point from the center of the box
    dist_far = (
                (dimensions['x']/2.0)**2.0 +
                (dimensions['y']/2.0)**2.0 +
                (dimensions['z']/2.0)**2.0
                )**(0.5)

    # The volume with a radius of the fartherst point in the simulation box
    sphere_vol = 4.0/3.0*pi*dist_far**3.0

    # The distance interval for with data will be sampled
    delta_dist = dist_far/samples

    # Count the number of atoms between incrementing distances
    sample_data = {}
    for run in distance:
        dist = 0
        sample_data[run] = [0]*samples
        count_sample = 0
        incremental_dist = []
        incremental_vol = []
        while dist <= dist_far:
            count = 0
            for atom in distance[run]:
                if dist <= distance[run][count] < dist+delta_dist:
                    sample_data[run][count_sample] += 1

                count += 1

            count_sample += 1
            incremental_vol.append(
                                   4.0*pi*(dist+delta_dist)**2.0*delta_dist
                                   )
            dist += delta_dist
            incremental_dist.append(dist)  # Max distance from range

    for key in sample_data:
        count = 0
        for item in sample_data[key]:
            quotient = sample_data[key][count]*sphere_vol
            dividend = float(number_of_atoms)*incremental_vol[count]
            sample_data[key][count] = quotient/dividend
            count += 1

    for key in sample_data:
        print(len(sample_data[key]))
        print(sum(sample_data[key]))

    pl.plot(incremental_dist[:-1], sample_data[key])
    pl.show()
