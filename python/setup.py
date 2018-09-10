import os

# Getting the main data directory
first_directory = os.getcwd()
data_directory = first_directory+'/../data/'

# Getting the image directory
image_directory = first_directory+'/../images/'

# The directories were data will be saved
analysis = first_directory+'/../datacalculated/'
datamsd = analysis+'msd/'
datadiffusion = analysis+'diffusion/'
datardf = analysis+'rdf/'

# The directories were images will be saved for single runs
msd = image_directory+'msd/'
rdfplots = image_directory+'rdf/'

directories = [
               analysis,
               datamsd,
               datadiffusion,
               datardf,
               image_directory,
               msd,
               rdfplots,
               ]

for directory in directories:
    if not os.path.exists(directory):
        print('Creating directory: '+directory)
        os.makedirs(directory)
