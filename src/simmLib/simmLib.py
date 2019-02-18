import os
pathname = os.path.dirname(os.path.abspath(__file__))+'\\simm.jar'
os.environ['CLASSPATH'] = pathname

from jnius import autoclass
from jnius import JavaClass, MetaJavaClass

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

    def __init__(self, *args):
        if len(args) == 1:
            self.object = args[0]
        else:
            JavaSensitivity = autoclass('com.acadiasoft.im.simm.model.Sensitivity')
            productClass = args[0]
            riskType = args[1]
            qualifier = args[2]
            bucket = args[3]
            label1 = args[4]
            label2 = args[5]
            amount = args[6]
            amountCurrency = args[7]
            amountUSD = args[8]
            self.object = JavaSensitivity(String(productClass),
                                      String(riskType),
                                      String(qualifier),
                                      String(bucket),
                                      String(label1),
                                      String(label2),
                                      BigDecimal(str(amount)),
                                      String(amountCurrency),
                                      BigDecimal(str(amountUSD)))

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
        ScheduleProductClass = autoclass('com.acadiasoft.im.schedule.models.imtree.identifiers.ScheduleProductClass')
        LocalDate = autoclass('java.time.LocalDate')
        parOne = String(tradeId)
        parTwo = ScheduleProductClass.determineProductClass(productClass)
        [y, m, d] = list(map(int, valuationDate.split("-")))
        parThree = LocalDate.of(y, m, d)
        [y, m, d] = list(map(int, endDate.split("-")))
        parFour = LocalDate.of(y, m, d)
        parFive = BigDecimal(amount)
        parSix = String(amountCurrency)
        parSeven = BigDecimal(amountUSD)
        self.object = ScheduleNotional(parOne, parTwo, parThree, parFour, parFive, parSix, parSeven)

    def getEndDate(self):
        doM = self.object.getEndDate().getDayOfMonth()
        year = self.object.getEndDate().getYear()
        month = self.object.getEndDate().getMonthValue()
        return (str(year)+'-'+f'{month:02}'+'-' + f'{doM:02}')

    def getValuationDate(self):
        doM = self.object.getValuationDate().getDayOfMonth()
        year = self.object.getValuationDate().getYear()
        month = self.object.getValuationDate().getMonthValue()
        return (str(year) + '-' + f'{month:02}' + '-' + f'{doM:02}')

    def getAmountUsd(self):
        return self.object.getAmountUSD().doubleValue()

class SchedulePv(javaClass):

    def __init__(self, tradeId, productClass, valuationDate, endDate, amount, amountCurrency, amountUSD):
        SchedulePv = autoclass('com.acadiasoft.im.schedule.models.SchedulePv')
        self.object = SchedulePv(String(tradeId), String(productClass), String(str(valuationDate)), String(str(endDate)), String(str(amount)), String(amountCurrency), String(str(amountUSD)))

    def getEndDate(self):
        doM = self.object.getEndDate().getDayOfMonth()
        year = self.object.getEndDate().getYear()
        month = self.object.getEndDate().getMonthValue()
        return (str(year) + '-' + f'{month:02}' + '-' + f'{doM:02}')

    def getValuationDate(self):
        doM = self.object.getValuationDate().getDayOfMonth()
        year = self.object.getValuationDate().getYear()
        month = self.object.getValuationDate().getMonthValue()
        return (str(year) + '-' + f'{month:02}' + '-' + f'{doM:02}')

    def getAmountUsd(self):
        return self.object.getAmountUSD().doubleValue()