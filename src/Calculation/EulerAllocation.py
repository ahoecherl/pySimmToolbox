from CRIF.BumpedCrif import  BumpedCrif
from simmLib.simmLib import Simm, GenerateCsvString
from io import StringIO
import pandas as pd
from multiprocessing import Pool
import CRIF.CrifUtil

class EulerAllocation():

    DefaultEps = 0.001
    scaling = True
    DisplayEpsilon = 0.001
    parallelProcessing = False

    def calculate(imTree):
        imTree.EulerAllocationEps = EulerAllocation.DefaultEps
        trades = imTree.Crif.Sensitivities.keys()
        if EulerAllocation.parallelProcessing:
            # create tuples for multiprocess call:
            inputtuples = []
            for t in trades:
                inputtuples.append((imTree.Crif, imTree.CalculationCurrency, t, imTree.EulerAllocationEps))
            with Pool() as pool:
                bumpedFlatTrees = pool.starmap(EulerAllocation.createBumpedFlatTrees, inputtuples)
        else:
            bumpedFlatTrees = {}
            for t in trades:
                bumpedCrifs = BumpedCrif(imTree.Crif, t, imTree.EulerAllocationEps)
                javaTree = Simm.calculateTreeStandard(bumpedCrifs.getAllSensitivities(), imTree.CalculationCurrency)
                stringTree = GenerateCsvString.parseToFlatCsv(javaTree)
                stringTree = StringIO(stringTree)
                bumpedFlatTrees[t] = pd.read_csv(stringTree)
        result = EulerAllocation.eulerAllocationInTree(imTree, bumpedFlatTrees, imTree.EulerAllocationEps)
        return result

    def createBumpedFlatTrees(crif, calculationCurrency, tradeID, eps):
        bumpedCrif= BumpedCrif(crif, tradeID, eps)
        javaTree = Simm.calculateTreeStandard(bumpedCrif.getAllSensitivities(), calculationCurrency)
        stringTree = GenerateCsvString.parteToFlatCsv(javaTree)
        stringTree = StringIO(stringTree)
        result = pd.read_csv(stringTree)
        return {tradeID: result}

    def eulerAllocationInTree(origTree, bumpedFlatTrees, eps):
        eulerAllocationMatrix = pd.DataFrame()
        for t in bumpedFlatTrees.keys():
            eulerAllocationMatrix[t] = (bumpedFlatTrees[t].ExposureAmount - origTree.FlatTree.ExposureAmount) / eps
        for key, value in origTree.nodes.items():
            eulerAllocation = eulerAllocationMatrix.iloc[value.data.rowNumber]
            eulerAllocation = eulerAllocation[eulerAllocation.abs() > EulerAllocation.DisplayEpsilon]
            if EulerAllocation.scaling:
                Delta = eulerAllocation.sum() - value.data.ExposureAmount
                absSum = eulerAllocation.abs().sum()
                if absSum != 0:
                    DeltaT = Delta * (eulerAllocation.abs() / absSum)
                    eulerAllocation = eulerAllocation - DeltaT
            value.data.eulerAllocation = eulerAllocation
        origTree.hasEulerAllocation = True
        return origTree

def setDefaultEpsilon(eps):
    EulerAllocation.DefaultEps = eps

def setScaling(input):
    EulerAllocation.scaling = input

def setDisplayEpsilon(input):
    EulerAllocation.DisplayEpsilon = input