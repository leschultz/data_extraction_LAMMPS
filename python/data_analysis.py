import matplotlib.pyplot as pl
import pandas as pd
import argparse

parser = argparse.ArgumentParser(
                                 description='Terminal execution of the tool.',
                                 usage='Create plots.',
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 )
help_temperature_anneal = (
        """Plot the values for the annealing temperature
        """
        )

parser.add_argument(
                    '-n',
                    type=int,
                    nargs='+',
                    help=help_temperature_anneal
                    )

args = parser.parse_args()

for item1 in args.n:
    data = pd.read_csv(
                       '../data/txt/'+str(item1)+'.txt',
                       comment='#',
                       sep=' ',
                       skiprows=1,
                       header=None
                       )

    data.columns = ([
                     'Step',
                     'Temperature [K]',
                     'Pressure [bar]',
                     'Volume [A^3]',
                     'Potential Energy [eV]',
                     'Kinetic Energy [eV]'
                     ])

    for item2 in data.columns:
        pl.plot(data['Step'], data[item2])
        pl.xlabel('Step')
        pl.ylabel(str(item2))
        pl.legend([str(item1)+' [K]'])
        pl.grid(True)
        pl.savefig('../images/'+str(item1)+'_'+str(item2)+'temp_step')
        pl.clf()

    number_of_atoms =  pd.read_csv(
                                   '../data/lammpstrj/'+str(item1)+'_final.lammpstrj',
                                   skiprows=3,
                                   nrows=1,
                                   header=None
                                   )

    number_of_atoms = number_of_atoms[0][0]

    count = 0
    while (data['Temperature [K]'][count] <= item1):
        count += 1

    columns = ([
                'id',
                'type',
                'x',
                'y',
                'z',
                'junk'
                ])

    data1 = pd.read_csv(
                        '../data/lammpstrj/'+str(item1)+'_rate.lammpstrj',
                        comment='#',
                        sep=' ',
                        skiprows=9+(9+number_of_atoms)*count,
                        nrows=number_of_atoms,
                        header=None
                        )

    data1.columns = columns

    data2 = pd.read_csv(
                        '../data/lammpstrj/'+str(item1)+'_final.lammpstrj',
                        comment='#',
                        sep=' ',
                        skiprows=9,
                        header=None
                        )

    data2.columns = columns

    delta_x = data2['x']-data1['x']
    delta_y = data2['y']-data1['y']
    delta_z = data2['z']-data1['z']

    distance_traveled = (delta_x**2+delta_y**2+delta_z**2)**(1.0/2.0)
    print distance_traveled
