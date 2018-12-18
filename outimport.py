from itertools import islice
import pandas as pd


def readdata(filepath):

    with open(filepath) as file:
        for line in file:
            headers = line.strip().split(' ')

            if 'Step' in headers:
                break

    data = []
    with open(filepath) as file:
        for line in file:
            values = line.strip().split(' ')
            values = [i for i in values if '' is not i]

            try:
                if values:
                    values = [float(i) for i in values]
                    values[0] = int(values[0])
                    data.append(values)
            except Exception:
                pass

    df = pd.DataFrame(data, columns=headers)
    return df
