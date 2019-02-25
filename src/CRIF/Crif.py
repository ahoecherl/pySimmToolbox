from simmLib.simmLibUtils import *
from simmLib.simmLib import *

class Crif():

    def __init__(self, CRIFdataframe):
        self.Sensitivities = {}
        self.ScheduleNotionals = {}
        self.SchedulePVs = {}
        self.AddOnNotionalFactors = ArrayList()
        self.AddOnNotionals = {}
        self.ProductMultipliers = ArrayList()
        self.AddOnFixedAmounts = ArrayList()
        self.asDataFrame = CRIFdataframe
        if CRIFdataframe[['IMLedis','CollectRegulations','PostRegulations']].drop_duplicates().shape[0]>1:
            raise ValueError('IMLedis column of CRIF had more than one unique value. This function should only be called with the CRIF of a single Counterparty, direction and Regulation. Use Crifs instead.')
        else:
            self.Counterparty = CRIFdataframe.IMLedis.unique()[0]
            if CRIFdataframe.CollectRegulations.unique()[0] == '':
                self.direction = 'post'
                self.regulation = CRIFdataframe.PostRegulations.unique()[0]
            else:
                self.direction = 'collect'
                self.regulation = CRIFdataframe.CollectRegulations.unique()[0]
        for row in CRIFdataframe.itertuples():
            if (row.IMModel == 'Schedule' and row.riskType =='Notional'):
                scheduleNotional = createScheduleNotional(row.tradeId,
                                                    row.productClass,
                                                    row.ValuationDate,
                                                    row.EndDate,
                                                    row.amount,
                                                    row.amountCurrency,
                                                    row.amountUSD)
                if row.tradeId in self.ScheduleNotionals:
                    self.ScheduleNotionals[row.tradeId].add(scheduleNotional)
                else:
                    self.ScheduleNotionals[row.tradeId] = ArrayList(Arrays.asList(scheduleNotional))

            elif (row.IMModel == 'Schedule' and row.riskType =='PV'):
                schedulePV = createSchedulePv(row.tradeId,
                                        row.productClass,
                                        row.ValuationDate,
                                        row.EndDate,
                                        row.amount,
                                        row.amountCurrency,
                                        row.amountUSD
                                        )
                if row.tradeId in self.SchedulePVs:
                    self.SchedulePVs[row.tradeId].add(schedulePV)
                else:
                    self.SchedulePVs[row.tradeId] = ArrayList(Arrays.asList(schedulePV))

            elif (row.IMModel in ['SIMM-P','SIMM', ''] and row.riskType == 'Param_ProductClassMultiplier'):
                productMultiplier = createProductMultiplier(row.qualifier,
                                                      row.amount)
                self.ProductMultipliers.add(productMultiplier)

            elif row.riskType == 'Param_AddOnFixedAmount':
                addOnFixedAmount = createAddOnFixedAmount(row.amount,
                                                    row.amountCurrency,
                                                    row.amountUSD)
                self.AddOnFixedAmounts.add(addOnFixedAmount)

            elif row.riskType == 'Param_AddOnNotionalFactor':
                addOnNotionalFactor = createAddOnNotionalFactor(row.qualifier,
                                                          row.amountUSD)
                self.AddOnNotionalFactors.add(addOnNotionalFactor)

            elif (row.IMModel in ['SIMM-P','SIMM', ''] and row.riskType =='Notional'):
                addOnNotional = createAddOnNotional(row.qualifier,
                                              row.amount,
                                              row.amountCurrency,
                                              row.amountUSD)
                if row.tradeId in self.AddOnNotionals:
                    self.AddOnNotionals[row.tradeId].add(addOnNotional)
                else:
                    self.AddOnNotionals[row.tradeId] = ArrayList(Arrays.asList(addOnNotional))

            else:
                sensitivity = createSensitivity(row.productClass,
                                      row.riskType,
                                      row.qualifier,
                                      row.bucket,
                                      row.label1,
                                      row.label2,
                                      row.amount,
                                      row.amountCurrency,
                                      row.amountUSD)
                if row.tradeId in self.Sensitivities:
                    self.Sensitivities[row.tradeId].add(sensitivity)
                else:
                    self.Sensitivities[row.tradeId] = ArrayList(Arrays.asList(sensitivity))
        asdf = 1

    def getAllSensitivities(self):
        result = ArrayList()
        for key in self.Sensitivities:
            result.addAll(self.Sensitivities[key])
        return result

    def getAllScheduleNotionals(self):
        result = ArrayList()
        for key in self.ScheduleNotionals:
            result.addAll(self.ScheduleNotionals[key])
        return result

    def getAllSchedulePVs(self):
        result = ArrayList()
        for key in self.SchedulePVs:
            result.addAll(self.SchedulePVs[key])
        return result

    def getAllAddonNotionals(self):
        result = ArrayList()
        for key in self.AddOnNotionals:
            result.addAll(self.AddOnNotionals[key])
        return result

    def getAllAddOnNotionalFactors(self):
        result = ArrayList()
        result.addAll(self.AddOnNotionalFactors)
        return result

    def getAllAddOnFixedAmounts(self):
        result = ArrayList()
        result.addAll(self.AddOnFixedAmounts)
        return result

    def getAllProductMultipliers(self):
        result = ArrayList()
        result.addAll(self.ProductMultipliers)
        return result

    def __str__(self):
        return (self.Counterparty+"_"+self.direction+"_"+self.regulation)