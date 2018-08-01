from analysis import load_lammpstrj
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
        data = load_lammpstrj(
                              item1,
                              calculation_step,
                              number_of_atoms,
                              columns
                              )

        for key in dimensions:

            count = 0
            for item2 in data[key]:

                if data[key][count] < 0:
                    while data[key][count] < 0:
                        data[key][count] = (
                                            data[key][count] +
                                            dimensions[key]
                                            )

                elif data[key][count] > dimensions[key]:
                    while data[key][count] > dimensions[key]:
                        data[key][count] = (
                                            data[key][count] -
                                            dimensions[key]
                                            )

                else:
                    data[key][count] =  data[key][count]

                count += 1

        data_wrap[item1] = data

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

    # The distance interval for with data will be sampled
    delta_dist = dist_far/float(samples)

    # Count the number of atoms between incrementing distances
    sample_data = {}
    for run in distance:
        dist = 0
        sample_data[run] = [0]*samples
        count_sample = 0
        incremental_dist = []
        while dist <= dist_far:
            count = 0
            for atom in distance[run]:
                if dist <= distance[run][count] < dist+delta_dist:
                    sample_data[run][count_sample] += 1

                count += 1

            count_sample += 1
            dist += delta_dist
            incremental_dist.append(dist)  # Max distance from range

    shell_volumes = []
    for item in incremental_dist:
        shell_volumes.append(4.0*pi*item**2.0*delta_dist)

    for key in sample_data:
        count = 0
        for item in sample_data[key]:
            dividend1 = samples
            dividend2 = 4.0*pi*incremental_dist[count]**2.0*delta_dist
            dividend3 = shell_volumes[count]
            quotient = sample_data[key][count]
            dividend = dividend1  # *dividend2*dividend3
            sample_data[key][count] = quotient/dividend
            count += 1

        print(sum(sample_data[key]))

    print(shell_volumes)
