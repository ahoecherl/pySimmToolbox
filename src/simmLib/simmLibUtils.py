from simmLib.simmLib import *

#Sensitivity Object
def createSensitivity(*args):
    if len(args) == 1:
        return args[0]
    else:
        productClass = args[0]
        riskType = args[1]
        qualifier = args[2]
        bucket = args[3]
        label1 = args[4]
        label2 = args[5]
        amount = args[6]
        amountCurrency = args[7]
        amountUSD = args[8]
        return Sensitivity(String(productClass),
                           String(riskType),
                           String(qualifier),
                           String(bucket),
                           String(label1),
                           String(label2),
                           BigDecimal(String(str(amount))),
                           String(amountCurrency),
                           BigDecimal(String(str(amountUSD))))

def getSensitivityAmount(sensitivity):
    return sensitivity.getAmount().doubleValue()

#ProductMultiplier Object
def createProductMultiplier(productClass, multiplier):
    return ProductMultiplier(String(productClass),
                      BigDecimal(String(str(multiplier))))

def getProductMultiplierProductClass(productMultiplier):
    return productMultiplier.getProductClass().getLabel()

def getProductMultiplierMultiplier(productMultiplier):
    return productMultiplier.getMultiplier().doubleValue()

#AddOnNotionalFactor Object
def createAddOnNotionalFactor(product, factor):
    return AddOnNotionalFactor(String(product),
                               BigDecimal(factor))

def getAddOnNotionalFactorFactor(addOnNotionalFactor):
    return addOnNotionalFactor.getFactor().doubleValue()

#AddOnFixedAmount Object
def createAddOnFixedAmount(amount, currency, amountUsd):
    return AddOnFixedAmount(BigDecimal(String(str(amount))),
                            String(currency),
                            BigDecimal(String(str(amountUsd))))

def getAddOnFixedAmountAmountUsd(addOnFixedAmount):
    return addOnFixedAmount.getAmountUsd().doubleValue()

#AddOnNotional Object
def createAddOnNotional(product, notional, currency, notionalUsd):
    return AddOnNotional(String(product),
                         BigDecimal(String(str(notional))),
                         String(currency),
                         BigDecimal(String(str(notionalUsd))))

def getAddOnNotionalNotionalUsd(addOnNotional):
    return addOnNotional.getNotionalUsd().doubleValue()

#ScheduleNOtional Object
def createScheduleNotional(tradeId, productClass, valuationDate, endDate, amount, amountCurrency, amountUSD):
    [y, m, d] = list(map(int, valuationDate.split("-")))
    valuationDateJava = LocalDate.of(y, m, d)
    [y, m, d] = list(map(int, endDate.split("-")))
    endDateJava = LocalDate.of(y,m,d)
    return ScheduleNotional(String(tradeId),
                            ScheduleProductClass.determineProductClass(String(productClass)),
                            valuationDateJava,
                            endDateJava,
                            BigDecimal(String(str(amount))),
                            String(amountCurrency),
                            BigDecimal(String(str(amountUSD))))

def getScheduleNotionalEndDate(scheduleNotional):
    doM = scheduleNotional.getEndDate().getDayOfMonth()
    year = scheduleNotional.getEndDate().getYear()
    month = scheduleNotional.getEndDate().getMonthValue()
    return (str(year) + '-' + f'{month:02}' + '-' + f'{doM:02}')

def getScheduleNotionalValuationDate(scheduleNotional):
    doM = scheduleNotional.getValuationDate().getDayOfMonth()
    year = scheduleNotional.getValuationDate().getYear()
    month = scheduleNotional.getValuationDate().getMonthValue()
    return (str(year) + '-' + f'{month:02}' + '-' + f'{doM:02}')

def getScheduleNotionalAmountUsd(scheduleNotional):
    return scheduleNotional.getAmountUSD().doubleValue()

#SchedulePv Object:
def createSchedulePv(tradeId, productClass, valuationDate, endDate, amount, amountCurrency, amountUSD):
    [y, m, d] = list(map(int, valuationDate.split("-")))
    valuationDateJava = LocalDate.of(y, m, d)
    [y, m, d] = list(map(int, endDate.split("-")))
    endDateJava = LocalDate.of(y,m,d)
    return SchedulePv(String(tradeId),
                            ScheduleProductClass.determineProductClass(String(productClass)),
                            valuationDateJava,
                            endDateJava,
                            BigDecimal(String(str(amount))),
                            String(amountCurrency),
                            BigDecimal(String(str(amountUSD))))

def getSchedulePvEndDate(schedulePv):
    doM = schedulePv.getEndDate().getDayOfMonth()
    year = schedulePv.getEndDate().getYear()
    month = schedulePv.getEndDate().getMonthValue()
    return (str(year) + '-' + f'{month:02}' + '-' + f'{doM:02}')

def getSchedulePvValuationDate(schedulePv):
    doM = schedulePv.getValuationDate().getDayOfMonth()
    year = schedulePv.getValuationDate().getYear()
    month = schedulePv.getValuationDate().getMonthValue()
    return (str(year) + '-' + f'{month:02}' + '-' + f'{doM:02}')

def getSchedulePvAmountUsd(schedulePv):
    return schedulePv.getAmountUSD().doubleValue()