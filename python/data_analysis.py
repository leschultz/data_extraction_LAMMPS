import matplotlib.pyplot as pl
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Terminal execution of the tool.',
                                 usage='Create plots.',
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 )
help_temperature_anneal = (
        """Plot the values for the annealing temperature
        """
        )

parser.add_argument('-n',
                    type=int,
                    nargs='+',
                    help=help_temperature_anneal,
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
                     'Time Step [fs]',
                     'Temperature [K]',
                     'Pressure [bar]',
                     'Volume [A^3]',
                     'Potential Energy [eV]',
                     'Kinetic Energy [eV]'
                     ])

    for item2 in data.columns:

        pl.plot(data['Time Step [fs]'], data[item2], 'b.')
        pl.xlabel('Time Step [fs]')
        pl.ylabel(str(item2))
        pl.legend([str(item1)+' [K] annealing'])
        pl.grid(True)
        pl.savefig('../images/'+str(item1)+'_'+str(item2)+'temp_step')
        pl.clf()
