import os

# Getting the main data directory
first_directory = os.getcwd()
data_directory = first_directory+'/../data/'

# Getting the image directory
image_directory = first_directory+'/../images/'

# The directories were data will be saved
analysis = data_directory+'analysis/'
datamsd = analysis+'msd/'
datardf = analysis+'rdf/'
diffusion = analysis+'diffusion/'
cluster = analysis+'cluster/'
dat = data_directory+'dat/'
lammpstrj = data_directory+'lammpstrj/'
rest = data_directory+'rest/'
txt = data_directory+'txt/'

# The directories were images will be saved
motion = image_directory+'motion/'
system = image_directory+'system/'
rdf_plots = image_directory+'rdf/'
cluster_plots = image_directory+'cluster/'

directories = [
               analysis,
               datamsd,
               datardf,
               diffusion,
               cluster,
               dat,
               lammpstrj,
               rest,
               txt,
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
