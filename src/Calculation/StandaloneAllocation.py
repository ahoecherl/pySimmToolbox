from simmLib.simmLib import Simm, GenerateCsvString
import CRIF.CrifUtil
from io import StringIO
import pandas as pd
import ResultTrees.ImTreeUtil

class StandaloneAllocation():

    def calculate(imTree):
        trades = imTree.Crif.Sensitivities.keys()
        standaloneTrees = {}
        standaloneMatrix = imTree.FlatTree.copy(deep=True)
        standaloneMatrix.set_index(['Im Model', 'Silo', 'RiskClass', 'SensitivityType', 'Bucket', 'WeightedSensitivity'], inplace=True)
        standaloneMatrix.drop(columns=['ExposureAmount'], inplace=True)
        for t in trades:
            standaloneFlatTree = GenerateCsvString.parseToFlatCsv(Simm.calculateTreeStandard(imTree.Crif.Sensitivities[t], imTree.CalculationCurrency))
            standaloneFlatTree = StringIO(standaloneFlatTree)
            standaloneFlatTree = ResultTrees.ImTreeUtil.read_csv(standaloneFlatTree)
            standaloneFlatTree.set_index(['Im Model', 'Silo', 'RiskClass', 'SensitivityType', 'Bucket', 'WeightedSensitivity'], inplace=True)
            standaloneFlatTree.drop(columns =['Level'], inplace=True)
            standaloneFlatTree.rename(columns={'ExposureAmount':t}, inplace=True)
            standaloneMatrix = pd.merge(standaloneMatrix, standaloneFlatTree, how='left', on=['Im Model', 'Silo', 'RiskClass', 'SensitivityType', 'Bucket', 'WeightedSensitivity'])
        standaloneMatrix.drop(columns=['Level'], inplace=True)
        standaloneMatrix.reset_index(drop=True, inplace=True)

        for key, value in imTree.nodes.items():
            standaloneAllocation = standaloneMatrix.iloc[value.data.rowNumber]
            standaloneAllocation.dropna(inplace=True)
            value.data.standaloneAllocation = standaloneAllocation

        imTree.hasStandaloneAllocation = True

        return imTree