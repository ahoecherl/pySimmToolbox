from simmLib.simmLib import Simm, GenerateCsvString, Schedule
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

        if hasAddon:
            javaTree = Simm.calculateTreeTotal(crif.getAllSensitivities(),
                                               crif.getAllProductMultipliers(),
                                               crif.getAllAddOnNotionalFactors(),
                                               crif.getAllAddonNotionals(),
                                               crif.getAllAddOnFixedAmounts(),
                                               StandardCalculation.CalculationCurrency)

        else:
            javaTree = Simm.calculateTreeStandard(crif.getAllSensitivities(), StandardCalculation.CalculationCurrency)

        result = ImTree(GenerateCsvString.parseToFlatCsv(javaTree))
        result.CalculationCurrency = StandardCalculation.CalculationCurrency
        result.Crif = crif

        if hasSchedule:
            javaTreeSchedule = Schedule.calculateTree(crif.getAllScheduleNotionals(), crif.getAllSchedulePVs())
            result.addScheduleTree(GenerateCsvString.parseToFlatCsv(javaTreeSchedule))

        return result
    
def setCalculationCurrency(ccy):
    StandardCalculation.CalculationCurrency = ccy