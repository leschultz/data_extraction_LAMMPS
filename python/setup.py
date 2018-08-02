import glob
import os

# Getting the main data directory
first_directory = os.getcwd()
data_directory = first_directory+'/../data/'

# Getting the image directory
image_directory = first_directory+'/../images/'

# The directories were data will be saved
analysis = data_directory+'analysis/'
dat = data_directory+'dat/'
lammpstrj = data_directory+'lammpstrj/'
rest = data_directory+'rest/'
txt = data_directory+'txt/'
rdf = data_directory+'rdf/'

# The directories were images will be saved
motion = image_directory+'motion/'
system = image_directory+'system/'
rdf_plots = image_directory+'rdf/'

directories = [
               analysis,
               dat,
               lammpstrj,
               rest,
               txt,
               rdf,
               motion,
               system,
               rdf_plots
               ]


def check(directory):
    if not os.path.exists(directory):
        print('Creating directory: '+directory)
        os.makedirs(directory)


def delete(directory):
    filelist = glob.glob(os.path.join(directory, '*'))
    for item in filelist:
        os.remove(item)


def setup():
    '''The initial setup of needed directories'''

    for item in directories:
        check(item)


def clean():
    '''Clean data from previous runs'''

    for item in directories:
        delete(item)
