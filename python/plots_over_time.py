import matplotlib.pyplot as pl
import pandas as pd
import os

first_directory = os.getcwd()
txt_directory = first_directory+'/../data/txt/'

# The names of mean dislacements for each runi
txt_file_names = os.listdir(txt_directory)

# For each argument value generate graphs
for item1 in txt_file_names:
    data = pd.read_csv(
                       '../data/txt/'+str(item1),
                       comment='#',
                       sep=' ',
                       skiprows=1,
                       header=None
                       )

    # This is the orger of exported data
    data.columns = ([
                     'Step',
                     'Temperature [K]',
                     'Pressure [bar]',
                     'Volume [A^3]',
                     'Potential Energy [eV]',
                     'Kinetic Energy [eV]'
                     ])

    # This loops over each data plot type
    for item2 in data.columns:
        pl.plot(data['Step'], data[item2])
        pl.xlabel('Step')
        pl.ylabel(str(item2))
        pl.legend([str(item1)])
        pl.grid(True)
        pl.savefig('../images/system/'+str(item2)+'_'+str(item1)+'.png')
        pl.clf()
