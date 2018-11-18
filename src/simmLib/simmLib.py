import os
os.environ['CLASSPATH'] = r'C:\D-Fine\pySimmToolbox\src\simmLib\simm.jar'

from jnius import autoclass

String = autoclass('java.lang.String')
BigDecimal = autoclass('java.math.BigDecimal')

Simm = autoclass('com.acadiasoft.im.simm.engine.Simm')
Schedule = autoclass('com.acadiasoft.im.schedule.engine.Schedule')
Arrays = autoclass('java.util.Arrays')
ArrayList = autoclass('java.util.ArrayList')
GenerateCsvString = autoclass('com.acadiasoft.im.base.imtree.GenerateCsvString')


class javaClass():

    def getJavaObj(self):
        return self.object


class Sensitivity(javaClass):

    def __init__(self, productClass, riskType, qualifier, bucket, label1, label2, amount, amountCurrency, amountUSD):
        Sensitivity = autoclass('com.acadiasoft.im.simm.model.Sensitivity')
        self.object = Sensitivity(String(productClass),
                           String(riskType),
                           String(qualifier),
                           String(bucket),
                           String(label1),
                           String(label2),
                           BigDecimal(str(amount)),
                                  String(amountCurrency),
                                  BigDecimal(str(amount)))

    def getRiskType(self):
        return self.object.getRiskType()

    def getAmount(self):
        return self.object.getAmount().doubleValue()


class ProductMultiplier(javaClass):

    def __init__(self, productClass, multiplier):
        ProductMultiplier = autoclass('com.acadiasoft.im.simm.model.ProductMultiplier')
        self.object = ProductMultiplier(String(productClass),
                                        BigDecimal(str(multiplier)))

    def getProductClass(self):
        return self.object.getProductClass().getLabel()

    def getMultiplier(self):
        return self.object.getMultiplier().doubleValue()

class AddOnNotionalFactor(javaClass):

    def __init__(self, product, factor):
        AddOnNotionalFactor = autoclass('com.acadiasoft.im.simm.model.AddOnNotionalFactor')
        self.object = AddOnNotionalFactor(String(product), BigDecimal(factor))

    def getProduct(self):
        return self.object.getProduct()

    def getFactor(self):
        return self.object.getFactor().doubleValue()


class AddOnFixedAmount(javaClass):

    def __init__(self, amount, currency, amountUsd):
        AddOnFixedAmount = autoclass('com.acadiasoft.im.simm.model.AddOnFixedAmount')
        self.object = AddOnFixedAmount(BigDecimal(str(amount)), String(currency), BigDecimal(str(amountUsd)))

    def getCurrency(self):
        return self.object.getCurrency()

    def getAmountUsd(self):
        return self.object.getAmountUsd().doubleValue()


class AddOnNotional(javaClass):

    def __init__(self, product, notional, currency, notionalUsd):
        AddOnNotional = autoclass('com.acadiasoft.im.simm.model.AddOnNotional')
        self.object = AddOnNotional(String(product), BigDecimal(str(notional)), String(currency), BigDecimal(str(notionalUsd)))

    def getProduct(self):
        return self.object.getProduct()

    def getNotionalUsd(self):
        return  self.object.getNotionalUsd().doubleValue()


class ScheduleNotional(javaClass):

    def __init__(self, tradeId, productClass, valuationDate, endDate, amount, amountCurrency, amountUSD):
        ScheduleNotional = autoclass('com.acadiasoft.im.schedule.models.ScheduleNotional')
        self.object = ScheduleNotional(String(tradeId), String(productClass), String(str(valuationDate)), String(str(endDate)), String(str(amount)), String(amountCurrency), String(str(amountUSD)))

    def getEndDate(self):
        DateTimeFormatter = autoclass('java.time.format.DateTimeFormatter')
        LocalDate = autoclass('java.time.LocalDate')
        return self.object.getEndDate().format(DateTimeFormatter.ofPattern("yyyy-MM-dd"))

    def getAmountUsd(self):
        return self.object.getAmountUSD().doubleValue()

class SchedulePv(javaClass):

    def __init__(self, tradeId, productClass, valuationDate, endDate, amount, amountCurrency, amountUSD):
        SchedulePv = autoclass('com.acadiasoft.im.schedule.models.SchedulePv')
        self.object = SchedulePv(String(tradeId), String(productClass), String(str(valuationDate)), String(str(endDate)), String(str(amount)), String(amountCurrency), String(str(amountUSD)))

    def getEndDate(self):
        DateTimeFormatter = autoclass('java.time.format.DateTimeFormatter')
        LocalDate = autoclass('java.time.LocalDate')
        return self.object.getEndDate().format(DateTimeFormatter.ofPattern("yyyy-MM-dd"))

    def getAmountUsd(self):
        return self.object.getAmountUSD().doubleValue()