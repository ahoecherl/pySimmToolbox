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
                scheduleNotional = ScheduleNotional(row.tradeId,
                                                    row.productClass,
                                                    row.ValuationDate,
                                                    row.EndDate,
                                                    row.amount,
                                                    row.amountCurrency,
                                                    row.amountUSD)
                if row.tradeId in self.ScheduleNotionals:
                    self.ScheduleNotionals[row.tradeId].add(scheduleNotional.getJavaObj())
                else:
                    self.ScheduleNotionals[row.tradeId] = ArrayList(Arrays.asList(scheduleNotional.getJavaObj()))

            elif (row.IMModel == 'Schedule' and row.riskType =='PV'):
                schedulePV = SchedulePv(row.tradeId,
                                        row.productClass,
                                        row.ValuationDate,
                                        row.EndDate,
                                        row.amount,
                                        row.amountCurrency,
                                        row.amountUSD
                                        )
                if row.tradeId in self.SchedulePVs:
                    self.SchedulePVs[row.tradeId].add(schedulePV.getJavaObj())
                else:
                    self.SchedulePVs[row.tradeId] = ArrayList(Arrays.asList(schedulePV.getJavaObj()))

            elif (row.IMModel == 'SIMM-P' and row.riskType == 'Param_ProductClassMultiplier'):
                productMultiplier = ProductMultiplier(row.qualifier,
                                                      row.amount)
                self.ProductMultipliers.add(productMultiplier.getJavaObj())

            elif row.riskType == 'Param_AddOnFixedAmount':
                addOnFixedAmount = AddOnFixedAmount(row.amount,
                                                    row.amountCurrency,
                                                    row.amountUSD)
                self.AddOnFixedAmounts.add(addOnFixedAmount.getJavaObj())

            elif row.riskType == 'Param_AddOnNotionalFactor':
                addOnNotionalFactor = AddOnNotionalFactor(row.qualifier,
                                                          row.amountUSD)
                self.AddOnNotionalFactors.add(addOnNotionalFactor.getJavaObj())

            elif (row.IMModel == 'SIMM-P' and row.riskType =='Notional'):
                addOnNotional = AddOnNotional(row.qualifier,
                                              row.amount,
                                              row.amountCurrency,
                                              row.amountUSD)
                if row.tradeId in self.AddOnNotionals:
                    self.AddOnNotionals[row.tradeId].add(addOnNotional.getJavaObj())
                else:
                    self.AddOnNotionals[row.tradeId] = ArrayList(Arrays.asList(addOnNotional.getJavaObj()))

            else:
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