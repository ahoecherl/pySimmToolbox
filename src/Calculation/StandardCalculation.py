from simmLib.simmLib import Simm, GenerateCsvString
from ResultTrees.ImTree import ImTree
from io import StringIO

class StandardCalculation():
    
    CalculationCurrency = 'USD'
    
    def calculate(crif):
        hasSchedule = False
        hasAddon = False

        if crif.SchedulePVs or crif.ScheduleNotionals:
            hasSchedule = True

        if crif.AddOnNotionals or not crif.AddOnFixedAmounts.isEmpty() or not crif.ProductMultipliers.isEmpty():
            hasAddon = True

        if hasAddon and not hasSchedule:
            javaTree = Simm.calculateTreeTotal(crif.getAllSensitivities(), crif.getAllProductMultipliers(), crif.getAllAddOnNotionalFactors(), crif.getAllAddonNotionals(), crif.getAllAddOnFixedAmounts(), StandardCalculation.CalculationCurrency)
            test = Simm.calculateAdditional(crif.getAllSensitivities(), crif.getAllProductMultipliers(), crif.getAllAddOnNotionalFactors(), crif.getAllAddonNotionals(), crif.getAllAddOnFixedAmounts(), StandardCalculation.CalculationCurrency)
            asdf = 1

        else:
            javaTree = Simm.calculateTreeStandard(crif.getAllSensitivities(), StandardCalculation.CalculationCurrency)

        result = ImTree(GenerateCsvString.parseToFlatCsv(javaTree))
        result.CalculationCurrency = StandardCalculation.CalculationCurrency
        result.Crif = crif
        return result
    
def setCalculationCurrency(ccy):
    StandardCalculation.CalculationCurrency = ccy