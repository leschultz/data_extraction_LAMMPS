'''
This script creates needed directories to save data and images.
'''

import os


def exportdir(folder):
    '''
    Create a folder (with the path) where data is exported.
    '''

    # The directories were data will be saved
    analysis = folder+'/datacalculated/'
    datamsd = analysis+'msd/'
    datadiffusion = analysis+'diffusion/'
    datardf = analysis+'rdf/'
    dataerr = analysis+'errormethods/'
    dataset = analysis+'settlingindexes/'

    # The directories were images will be saved for single runs
    image_directory = folder+'/images/'
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
                   dataset
                   ]

    # Create directories if they do not exist
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
