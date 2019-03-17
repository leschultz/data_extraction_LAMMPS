from shutil import copy

import tarfile
import os


def copydata(item):
    '''
    Copy the data for Tg analysis.

    inputs:
        item = The path for where data may be

    outputs:
        A collection of data files
    '''

    if 'job' in item[0]:

        # Were parsed data will be stored
        data = []

        # Create a name from the path
        name = item[0].split('/')
        name = name[-4:]
        name = os.path.join(*name)

        # Print status
        print('Copying data: '+name)

        savepath = os.path.join(*['./', name])

        condition = ('dep.in' in item[-1])

        # Grab the output if the file exists
        if ('test.out' in item[-1]) & condition:
            filename = os.path.join(*[item[0], 'test.out'])
            inputfile = os.path.join(*[item[0], 'dep.in'])

            # Create the path to work in
            if not os.path.exists(name):
                os.makedirs(name)

            copy(inputfile, savepath)
            copy(filename, savepath)

        # Grab the output archive file that contains run system data
        elif ('outputs.tar.gz' in item[-1]) & condition:
            filename = os.path.join(*[item[0], 'outputs.tar.gz'])
            inputfile = os.path.join(*[item[0], 'dep.in'])

            # Open the archive
            archive = tarfile.open(filename, 'r')

            # Iterate for each file in the archive
            for member in archive.getmembers():

                # Open the file containing system data
                if 'test.out' in str(member):
                    member = archive.extractfile(member)
                    content = member.read()

            # Create the path to work in
            if not os.path.exists(name):
                os.makedirs(name)

            copy(inputfile, savepath)
            open(savepath+'/test.out', 'wb').write(content)

        print('-'*79)


def jobiterator(path):
    '''
    Search for all possible files to copy for Tg analysis.

    inputs:
        path = The path with all the runs

    outputs:
        A collection of data files
    '''

    # Look for all directories as generator object
    paths = os.walk(path)

    # Loop for each path
    for item in paths:
        copydata(item)


# The path to the google drive data
path = '/home/nerve/Documents/UW/gdrive/DMREF/MD/Rc_database/TEMP/'

jobiterator(path)
