import pandas as pd

def read_csv(path, sep=','):
    dtypes = {'ValuationDate': str,
              'Counterparty': str,
              'IMLedis': str,
              'tradeId': str,
              'TradeID': str,
              'productClass': str,
              'ProductClass': str,
              'riskType': str,
              'RiskType': str,
              'qualifier': str,
              'Qualifier': str,
              'bucket': str,
              'Bucket': str,
              'label1': str,
              'Label1': str,
              'label2': str,
              'Label2': str,
              'amount': float,
              'Amount': float,
              'amountCurrency': str,
              'AmountCurrency': str,
              'amountUSD': float,
              'AmountUSD': float,
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
                                      'tradeID':'tradeId',
                                      'Counterparty':'IMLedis',
                                      'ProductClass':'productClass',
                                      'RiskType': 'riskType',
                                      'Qualifier': 'qualifier',
                                      'Bucket': 'bucket',
                                      'Label1': 'label1',
                                      'Label2': 'label2',
                                      'Amount': 'amount',
                                      'AmountUSD': 'amountUSD',
                                      'AmountCurrency': 'amountCurrency',
                                      'TradeID': 'tradeId'}
                  , inplace=True)
    if 'ValuationDate' in result:
        temp = pd.to_datetime(result.ValuationDate).dt.strftime('%Y-%m-%d')
        temp.replace('NaT', '', inplace=True)
        result['ValuationDate'] = temp
    if 'EndDate' in result:
        temp2 = pd.to_datetime(result.EndDate).dt.strftime('%Y-%m-%d')
        temp2.replace('NaT', '', inplace=True)
        result['EndDate'] = temp2
    # If Collect and Post Regulations does not exist insert a Collect Regulations Column that is always EMIR and a post Regulations Collumn that is always empty.
    if not ('PostRegulations' in result or 'CollectRegulations' in result):
        result['CollectRegulations'] = 'EMIR'
        result['PostRegulations'] = ''
    if not 'IMModel' in result:
        result['IMModel'] = 'SIMM-P'
    result = result.fillna('')
    return result