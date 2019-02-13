import pandas as pd

def read_csv(path, sep=','):
    dtypes = {'Bucket': str}
    result = pd.read_csv(path, sep=sep, dtype=dtypes)
    result = result.fillna('')
    return result