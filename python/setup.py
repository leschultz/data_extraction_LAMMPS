import os

# Getting the main data directory
first_directory = os.getcwd()
data_directory = first_directory+'/../data/'

# Getting the image directory
image_directory = first_directory+'/../images/'

# The directories were data will be saved
analysis = first_directory+'/../datacalculated/'
datamsd = analysis+'msd/'
diffusion = analysis+'diffusion/'
cluster = analysis+'cluster/'

# The directories were images will be saved
motion = image_directory+'motion/'
system = image_directory+'system/'
rdf_plots = image_directory+'rdf/'
cluster_plots = image_directory+'cluster/'

directories = [
               analysis,
               datamsd,
               diffusion,
               cluster,
               motion,
               system,
               rdf_plots,
               cluster_plots
               ]


def check(directory):
    if not os.path.exists(directory):
        print('Creating directory: '+directory)
        os.makedirs(directory)


for item in directories:
    check(item)
