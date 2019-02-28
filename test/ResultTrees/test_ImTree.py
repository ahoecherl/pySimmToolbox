import unittest
from ResultTrees.ImTree import ImTree
import CRIF.CrifUtil
import time
from CRIF.Crif import Crif
from CRIF.Crifs import Crifs
from io import StringIO
from Calculation.StandardCalculation import StandardCalculation
from Calculation.EulerAllocation import EulerAllocation
from Calculation.StandaloneAllocation import StandaloneAllocation
from CRIF.Crifs import Crifs

class ImTreeTest(unittest.TestCase):

    def testCrifTree(self):
        exTreeString= '''Level,Im Model,Silo,RiskClass,SensitivityType,Bucket,WeightedSensitivity,ExposureAmount
1.Total,Total,,,,,,2023872525.630011
2.ImModel,SIMM-P,,,,,,2023872525.630011
3.Silo,SIMM-P,RatesFX,,,,,2023872525.630011
4.Risk Class,SIMM-P,RatesFX,Interest Rate,,,,2023872525.630011
5.Sensitivity Type,SIMM-P,RatesFX,Interest Rate,Delta,,,2023872525.630011
6.Bucket,SIMM-P,RatesFX,Interest Rate,Delta,JPY,,2023872525.630011'''
        crifTree = ImTree(exTreeString)
        self.assertAlmostEqual(2023872525.630011, crifTree.get_node(0).data.ExposureAmount, places=2)
        self.assertEqual(crifTree.get_node(2).data.identifier, 'SIMM-P_RatesFX')
        self.assertEqual(crifTree.get_node(crifTree.get_node(5).bpointer).data.identifier, 'SIMM-P_RatesFX_Interest Rate_Delta')
        asdf=1

    def testJsonCreatorStandardCalculation(self):
        OneLineCrif = '''ValuationDate,IMLedis,tradeId,IMModel,productClass,riskType,qualifier,bucket,label1,label2,amount,amountCurrency,amountUSD,EndDate,CollectRegulations,PostRegulations
,IMLedis_NRW_Bank,DZ14788807,SIMM,RatesFX,Risk_IRCurve,EUR,1,10y,Libor3m,1000000,EUR,1000000,,EMIR,'''
        Input = CRIF.CrifUtil.read_csv(StringIO(OneLineCrif))
        crif = Crif(Input)
        imTree = StandardCalculation.calculate(crif)
        testJson = imTree.to_json(with_data=True)
        self.assertEqual(testJson, r'''{"Total 51000000": {"children": [{"SIMM-P 51000000": {"children": [{"RatesFX 51000000": {"children": [{"Interest Rate 51000000": {"children": [{"Delta 51000000": {"children": [{"EUR 51000000": {"data": {"rowNumber": 5, "Level": 6, "levelName": "Bucket", "ExposureAmount": 51000000.0, "manifestation": "EUR", "identifier": "SIMM-P_RatesFX_Interest Rate_Delta_EUR"}}}], "data": {"rowNumber": 4, "Level": 5, "levelName": "Sensitivity Type", "ExposureAmount": 51000000.0, "manifestation": "Delta", "identifier": "SIMM-P_RatesFX_Interest Rate_Delta"}}}], "data": {"rowNumber": 3, "Level": 4, "levelName": "Risk Class", "ExposureAmount": 51000000.0, "manifestation": "Interest Rate", "identifier": "SIMM-P_RatesFX_Interest Rate"}}}], "data": {"rowNumber": 2, "Level": 3, "levelName": "Silo", "ExposureAmount": 51000000.0, "manifestation": "RatesFX", "identifier": "SIMM-P_RatesFX"}}}], "data": {"rowNumber": 1, "Level": 2, "levelName": "ImModel", "ExposureAmount": 51000000.0, "manifestation": "SIMM-P", "identifier": "SIMM-P"}}}], "data": {"rowNumber": 0, "Level": 1, "levelName": "Total", "ExposureAmount": 51000000.0, "manifestation": "Total", "identifier": ""}}}''')

    def test_toDataFrameOneLine(self):
        OneLineCrif = '''ValuationDate,IMLedis,tradeId,IMModel,productClass,riskType,qualifier,bucket,label1,label2,amount,amountCurrency,amountUSD,EndDate,CollectRegulations,PostRegulations
,IMLedis_NRW_Bank,DZ14788807,SIMM,RatesFX,Risk_IRCurve,EUR,1,10y,Libor3m,1000000,EUR,1000000,,EMIR,'''
        Input = CRIF.CrifUtil.read_csv(StringIO(OneLineCrif))
        crif = Crif(Input)
        imTree = StandardCalculation.calculate(crif)
        df = imTree.toDataFrame()
        asdf = 1

    def test_toDataFrameMultiLine(self):
        Input = CRIF.CrifUtil.read_csv(r'..\NochKleineresTestportfolio.csv')
        crif = Crif(Input)
        imTree = StandardCalculation.calculate(crif)
        df = imTree.toDataFrame()

    def test_toDataFrameBig(self):
        Input = CRIF.CrifUtil.read_csv(r'..\Testdatensatz1_CRIF.csv')
        crifs = Crifs(Input)
        crif = crifs.get(next(iter(crifs)))
        imTree = StandardCalculation.calculate(crif)
        df = imTree.toDataFrame()
        imTree.printToCsv(r'..\ExampleTreeAsCsv.csv')

    def test_toDataFrameWithEuler(self):
        Input = CRIF.CrifUtil.read_csv(r'..\NochKleineresTestportfolio.csv')
        crif = Crif(Input)
        imTree = StandardCalculation.calculate(crif)
        imTree = EulerAllocation.calculate(imTree)
        df = imTree.toDataFrame()

    def test_toDataFrameWithStandalone(self):
        Input = CRIF.CrifUtil.read_csv(r'..\NochKleineresTestportfolio.csv')
        crif = Crif(Input)
        imTree = StandardCalculation.calculate(crif)
        imTree = StandaloneAllocation.calculate(imTree)
        df = imTree.toDataFrame()

    def test_toDataFrameWithBothAllocations(self):
        Input = CRIF.CrifUtil.read_csv(r'..\NochKleineresTestportfolio.csv')
        crif = Crif(Input)
        imTree = StandardCalculation.calculate(crif)
        imTree = StandaloneAllocation.calculate(imTree)
        imTree = EulerAllocation.calculate(imTree)
        df = imTree.toDataFrame()
        asdf = 1

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
