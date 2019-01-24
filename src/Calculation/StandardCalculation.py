from simmLib.simmLib import Simm, GenerateCsvString
from ResultTrees.ImTree import ImTree
from io import StringIO

class StandardCalculation():
    
    CalculationCurrency = 'USD'
    
    def calculate(Crif):
        javaTree = Simm.calculateTreeStandard(Crif.getAllSensitivities(), StandardCalculation.CalculationCurrency)
        result = ImTree(GenerateCsvString.parseToFlatCsv(javaTree))
        result.CalculationCurrency = StandardCalculation.CalculationCurrency
        result.Crif = Crif
        return result
    
def setCalculationCurrency(ccy):
    StandardCalculation.CalculationCurrency = ccy