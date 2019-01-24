import pandas as pd

def read_csv(path, sep=','):
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
              'PostRegulations': str,
              'postRegulations': str,
              'collectRegulations': str,
              'crifNo': str,
              'valuationDate': str,
              'endDate': str}


    result = pd.read_csv(path, sep=sep, dtype=dtypes)
    result.rename(index=str, columns={'valuationDate':'ValuationDate',
                                      'crifNo':'IMLedis','endDate':'EndDate',
                                      'postRegulations':'PostRegulations',
                                      'collectRegulations':'CollectRegulations',
                                      'imModel':'IMModel',
                                      'tradeID':'tradeId'}
                  , inplace=True)
    temp = pd.to_datetime(result.ValuationDate).dt.strftime('%Y-%m-%d')
    temp.replace('NaT', '', inplace=True)
    result['ValuationDate'] = temp
    temp2 = pd.to_datetime(result.EndDate).dt.strftime('%Y-%m-%d')
    temp2.replace('NaT', '', inplace=True)
    result['EndDate'] = temp2
    result = result.fillna('')
    return result