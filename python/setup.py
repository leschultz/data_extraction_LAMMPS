import os

# Getting the main data directory
first_directory = os.getcwd()
data_directory = first_directory+'/../data/'

# The directories were data will be saved
analysis = first_directory+'/../datacalculated/'
datamsd = analysis+'msd/'
datadiffusion = analysis+'diffusion/'
datardf = analysis+'rdf/'

# The directories were images will be saved for single runs
image_directory = first_directory+'/../images/'
msdplots = image_directory+'msd/'
rdfplots = image_directory+'rdf/'
diffusionplots = image_directory+'diffusion/'

directories = [
               analysis,
               datamsd,
               datadiffusion,
               datardf,
               image_directory,
               msdplots,
               rdfplots,
               diffusionplots,
               ]

for directory in directories:
    if not os.path.exists(directory):
        print('Creating directory: '+directory)
        os.makedirs(directory)
