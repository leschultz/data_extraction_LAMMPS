'''
This script creates needed directories to save data and images.
'''

import os


def exportdir(folder):
    '''
    Create a folder (with the path) where data is exported.
    '''

    # Getting the main data directory
    first_directory = folder

    # The directories were data will be saved
    analysis = first_directory+'/datacalculated/'
    datamsd = analysis+'msd/'
    datadiffusion = analysis+'diffusion/'
    datardf = analysis+'rdf/'
    dataerr = analysis+'errormethods/'
    datasettling = analysis+'settling/'

    # The directories were images will be saved for single runs
    image_directory = first_directory+'/images/'
    msdplots = image_directory+'msd/'
    rdfplots = image_directory+'rdf/'
    diffusionplots = image_directory+'diffusion/'
    dataerrplots = image_directory+'errormethods/'
    correlationplot = dataerrplots+'autocorrelation/'
    errors = dataerrplots+'errors/'
    settling = image_directory+'settling/'

    directories = [
                   analysis,
                   datamsd,
                   datadiffusion,
                   datardf,
                   dataerr,
                   image_directory,
                   msdplots,
                   rdfplots,
                   diffusionplots,
                   dataerrplots,
                   correlationplot,
                   errors,
                   settling,
                   datasettling
                   ]

    # Create directories if they do not exist
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
