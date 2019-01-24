import unittest
from ResultTrees.ImTree import ImTree

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
        asdf=1