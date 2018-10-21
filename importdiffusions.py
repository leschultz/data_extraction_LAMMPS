import pandas as pd
import os


def filesdiff(maindir):
    folders = os.listdir(maindir)

    paths = {}
    for folder in folders:
        paths[folder] = {}

        filepath = maindir+folder+'/datacalculated/diffusion/'
        files = os.listdir(filepath)

        origins = [filepath+i for i in files if 'origin' in i]
        regular = [filepath+i for i in files if 'origin' not in i]

        paths[folder]['origins'] = origins
        paths[folder]['regular'] = regular

    regular = []
    origins = []
    for folder in paths:
        for item in paths[folder]['regular']:
            temp = item.split('_')[-1]
            temp = float(temp[:-1])
            df = pd.read_csv(item, sep=' ')
            df['temp'] = temp
            df['run'] = folder
            regular.append(df)

        for item in paths[folder]['origins']:
            temp = item.split('_')[-2]
            temp = float(temp[:-1])
            df = pd.read_csv(item, sep=' ')
            df['temp'] = temp
            df['run'] = folder
            origins.append(df)

    regular = pd.concat(regular, ignore_index=True)
    origins = pd.concat(origins, ignore_index=True)

    return regular, origins
