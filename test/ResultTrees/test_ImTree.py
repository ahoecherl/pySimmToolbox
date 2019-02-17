import unittest
from ResultTrees.ImTree import ImTree
import CRIF.CrifUtil
import time
from CRIF.Crif import Crif
from Calculation.StandardCalculation import StandardCalculation
from Calculation.EulerAllocation import EulerAllocation
from Calculation.StandaloneAllocation import StandaloneAllocation
from CRIF.Crifs import Crifs

class ImTreeTest(unittest.TestCase):

    def setUp(self):
        self.exTreeString = '''Level,Im Model,Silo,RiskClass,SensitivityType,Bucket,WeightedSensitivity,ExposureAmount
1.Total,Total,,,,,,2023872525.630011
2.ImModel,SIMM-P,,,,,,2023872525.630011
3.Silo,SIMM-P,RatesFX,,,,,2023872525.630011
4.Risk Class,SIMM-P,RatesFX,Interest Rate,,,,2023872525.630011
5.Sensitivity Type,SIMM-P,RatesFX,Interest Rate,Delta,,,2023872525.630011
6.Bucket,SIMM-P,RatesFX,Interest Rate,Delta,JPY,,2023872525.630011'''

    def testCrifTree(self):
        crifTree = ImTree(self.exTreeString)
        self.assertAlmostEqual(2023872525.630011, crifTree.get_node(0).data.ExposureAmount, places=2)
        self.assertEqual(crifTree.get_node(2).data.identifier, 'SIMM-P_RatesFX')
        self.assertEqual(crifTree.get_node(crifTree.get_node(5).bpointer).data.identifier, 'SIMM-P_RatesFX_Interest Rate_Delta')
        asdf=1

    # def test_Ausgabe(self):
    #     Input = CRIF.CrifUtil.read_csv(r'../LarsCRIF_DayBefore.csv')
    #     tic = time.time()
    #     crif = Crif(Input)
    #     imTree = StandardCalculation.calculate(crif)
    #     imTree = EulerAllocation.calculate(imTree)
    #     imTree = StandaloneAllocation.calculate(imTree)
    #     imTree.printToCsv(r'../LarsTestTreeAusgabeDayBefore.csv')
    #     toc = time.time()
    #     print(toc-tic)
    #     asdf = 1
    #
    #
    # def test_Ausgabe2(self):
    #     Input = CRIF.CrifUtil.read_csv(r'../UnitTest_Euler.csv')
    #     crifs = Crifs(Input)
    #     for key, crif in crifs.items():
    #         imTree = StandardCalculation.calculate(crif)
    #         imTree = EulerAllocation.calculate(imTree)
    #         imTree = StandaloneAllocation.calculate(imTree)
    #         imTree.printToCsv(r'../EulerUnitTest_'+key+'.csv')
