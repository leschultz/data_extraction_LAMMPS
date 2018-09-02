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

# The directories were images will be saved for single runs
singleimage = image_directory+'single/'
motionsingle = singleimage+'motion/'
systemsingle = singleimage+'system/'
rdfplotssingle = singleimage+'rdf/'
clusterplotssingle = singleimage+'cluster/'

# The directories were images will be saved for averaged runs
avgimage = image_directory+'averaged/'
motionavg = avgimage+'motion/'
clusteravg = avgimage+'cluster/'
diffusionavg = avgimage+'diffusion/'

directories = [
               analysis,
               datamsd,
               diffusion,
               cluster,
               singleimage,
               motionsingle,
               systemsingle,
               rdfplotssingle,
               clusterplotssingle,
               avgimage,
               motionavg,
               clusteravg,
               diffusionavg
               ]

for directory in directories:
    if not os.path.exists(directory):
        print('Creating directory: '+directory)
        os.makedirs(directory)
