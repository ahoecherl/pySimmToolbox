from simmLib.simmLib import *

class Crif():

    def __init__(self, CRIFdataframe):
        self.Sensitivities = {}
        self.asDataFrame = CRIFdataframe
        if CRIFdataframe[['IMLedis','CollectRegulations','PostRegulations']].drop_duplicates().shape[0]>1:
            raise ValueError('IMLedis column of CRIF had more than one unique value. This function should only be called with the CRIF of a single Counterparty, direction and Regulation. Use Crifs instead.')
        else:
            self.Counterparty = CRIFdataframe.IMLedis.unique()[0]
            if type(CRIFdataframe.CollectRegulations.unique()[0]) is str:
                self.direction = 'collect'
                self.regulation = CRIFdataframe.CollectRegulations.unique()[0]
            else:
                self.direction = 'post'
                self.regulation = CRIFdataframe.PostRegulations.unique()[0]
        for row in CRIFdataframe.itertuples():
            sensitivity = Sensitivity(row.productClass,
                                      row.riskType,
                                      row.qualifier,
                                      row.bucket,
                                      row.label1,
                                      row.label2,
                                      row.amount,
                                      row.amountCurrency,
                                      row.amountUSD)
            if row.tradeId in self.Sensitivities:
                self.Sensitivities[row.tradeId].add(sensitivity.getJavaObj())
            else:
                self.Sensitivities[row.tradeId] = ArrayList(Arrays.asList(sensitivity.getJavaObj()))
        asdf = 1

    def getAllSensitivities(self):
        result = ArrayList()
        for key in self.Sensitivities:
            result.addAll(self.Sensitivities[key])
        return result