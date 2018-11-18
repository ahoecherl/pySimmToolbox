import pandas as pd

def read_csv(path):
    dtypes = {'ValuationDate': str,
              'IMLedis': str,
              'tradeId': str,
              'productClass': str,
              'riskType': str,
              'qualifier': str,
              'bucket': str,
              'label1': str,
              'label2': str,
              'amount': float,
              'amountCurrency': str,
              'amountUSD': float,
              'EndDate': str,
              'CollectRegulations': str,
              'PostRegulations': str}

    result = pd.read_csv(path, sep=',', dtype=dtypes)
    result = result.fillna('')
    asdf = 1
    return result