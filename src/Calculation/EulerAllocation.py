from CRIF.BumpedCrif import  BumpedCrif
from simmLib.simmLib import Simm, GenerateCsvString
from io import StringIO
import pandas as pd
import CRIF.CrifUtil

class EulerAllocation():

    DefaultEps = 0.01
    scaling = False
    DisplayEpsilon = 0.001

    def calculate(imTree):
        imTree.EulerAllocationEps = EulerAllocation.DefaultEps
        trades = imTree.Crif.Sensitivities.keys()
        bumpedFlatTrees = {}
        for t in trades:
            bumpedCrifs = BumpedCrif(imTree.Crif, t, imTree.EulerAllocationEps)
            javaTree = Simm.calculateTreeStandard(bumpedCrifs.getAllSensitivities(), imTree.CalculationCurrency)
            stringTree = GenerateCsvString.parseToFlatCsv(javaTree)
            stringTree = StringIO(stringTree)
            bumpedFlatTrees[t] = pd.read_csv(stringTree)
        result = EulerAllocation.eulerAllocationInTree(imTree, bumpedFlatTrees, imTree.EulerAllocationEps)
        return result

    def eulerAllocationInTree(origTree, bumpedFlatTrees, eps):
        eulerAllocationMatrix = pd.DataFrame()
        for t in bumpedFlatTrees.keys():
            eulerAllocationMatrix[t] = (bumpedFlatTrees[t].ExposureAmount - origTree.FlatTree.ExposureAmount) / eps
        for key, value in origTree.nodes.items():
            eulerAllocation = eulerAllocationMatrix.iloc[value.data.rowNumber]
            eulerAllocation = eulerAllocation[eulerAllocation.abs() > EulerAllocation.DisplayEpsilon]
            if EulerAllocation.scaling:
                eulerAllocation = eulerAllocation * (value.data.ExposureAmount/eulerAllocation.sum())
            value.data.eulerAllocation = eulerAllocation
        origTree.hasEulerAllocation = True
        return origTree

def setDefaultEpsilon(eps):
    EulerAllocation.DefaultEps = eps

def setScaling(input):
    EulerAllocation.scaling = input

def setDisplayEpsilon(input):
    EulerAllocation.DisplayEpsilon = input