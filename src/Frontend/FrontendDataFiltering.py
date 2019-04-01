import pandas as pd

def getIM(dataframe):
    return dataframe.iloc[0][10]

def getNodeStandaloneAlloc(dataframe, node):
    filtered = dataframe[(dataframe.AllocationType == 'Standalone') & (dataframe.identifier==int(node))]
    forSeries = filtered[['tradeID', 'ExposureAmount']]
    resultSeries = pd.Series(data= filtered.ExposureAmount.values, index= filtered.tradeID.values)
    resultSeries = resultSeries.sort_values(ascending=False)
    return resultSeries

def getNodeEulerPosAlloc(dataframe, node):
    filtered = dataframe[(dataframe.AllocationType == 'Euler') & (dataframe.identifier == int(node)) & (dataframe.ExposureAmount>=0)]
    forSeries = filtered[['tradeID', 'ExposureAmount']]
    resultSeries = pd.Series(data=filtered.ExposureAmount.values, index=filtered.tradeID.values)
    resultSeries = resultSeries.sort_values(ascending=False)
    return resultSeries

def getNodeEulerNegAlloc(dataframe, node):
    filtered = dataframe[(dataframe.AllocationType == 'Euler') & (dataframe.identifier == int(node)) & (dataframe.ExposureAmount<0)]
    resultSeries = pd.Series(data=filtered.ExposureAmount.values, index=filtered.tradeID.values)
    resultSeries = resultSeries.sort_values(ascending=True)
    return resultSeries