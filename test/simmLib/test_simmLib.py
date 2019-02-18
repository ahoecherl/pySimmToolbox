import unittest
from simmLib.simmLib import *

class simmLibTest(unittest.TestCase):

    def test_Sensitivity(self):
        sensitivity = Sensitivity('RatesFX', 'Risk_FX', 'CHF', '', '', '', 12, 'USD', 12)
        self.assertEqual('Risk_FX', sensitivity.getRiskType())
        self.assertAlmostEqual(12, sensitivity.getAmount())

    def test_ProductMultiplier(self):
        productMultiplier = ProductMultiplier('RatesFX', 1.205)
        self.assertEqual('RatesFX', productMultiplier.getProductClass())
        self.assertAlmostEqual(1.205, productMultiplier.getMultiplier())

    def test_AddOnNotionalFactor(self):
        addOnNotionalFactor = AddOnNotionalFactor('ProductOne', 6.105)
        self.assertEqual('ProductOne', addOnNotionalFactor.getProduct())
        self.assertAlmostEqual(6.105, addOnNotionalFactor.getFactor())

    def test_AddOnFixedAmount(self):
        addOnFixedAmount = AddOnFixedAmount(130, 'EUR', 150)
        self.assertEqual('EUR', addOnFixedAmount.getCurrency())
        self.assertAlmostEqual(150, addOnFixedAmount.getAmountUsd())

    def test_AddOnNotional(self):
        addOnNotional = AddOnNotional('ProductOne', 180, 'EUR', 210)
        self.assertEqual(addOnNotional.getProduct(), 'ProductOne')
        self.assertAlmostEqual(addOnNotional.getNotionalUsd(), 210)

    def test_ScheduleNotional(self):
        scheduleNotional = ScheduleNotional('trade1', 'Rates', '2018-09-12', '2018-11-23', 1000, 'EUR', 1200)
        self.assertEqual('2018-11-23', scheduleNotional.getEndDate())
        self.assertAlmostEqual(1200, scheduleNotional.getAmountUsd())
        self.assertEqual('2018-09-12', scheduleNotional.getValuationDate())
        self.assertEqual('trade1', scheduleNotional.getJavaObj().getTradeId())
        self.assertAlmostEqual(1000, scheduleNotional.getJavaObj().getAmount().doubleValue(), places=3)

    def test_SchedulePv(self):
        schedulePv = SchedulePv('trade1', 'Rates', '2018-09-12', '2018-11-23', 1000, 'EUR', 1200)
        self.assertEqual('2018-11-23', schedulePv.getEndDate())
        self.assertAlmostEqual(1200, schedulePv.getAmountUsd())
        self.assertEqual('2018-09-12', schedulePv.getValuationDate())
        self.assertEqual('trade1', schedulePv.getJavaObj().getTradeId())
        self.assertAlmostEqual(1000, schedulePv.getJavaObj().getAmount().doubleValue(), places=3)

    def testIR7tree(self):
        treeRes = '''Level,Im Model,Silo,RiskClass,SensitivityType,Bucket,WeightedSensitivity,ExposureAmount
1.Total,Total,,,,,,2023872525.630011
2.ImModel,SIMM-P,,,,,,2023872525.630011
3.Silo,SIMM-P,RatesFX,,,,,2023872525.630011
4.Risk Class,SIMM-P,RatesFX,Interest Rate,,,,2023872525.630011
5.Sensitivity Type,SIMM-P,RatesFX,Interest Rate,Delta,,,2023872525.630011
6.Bucket,SIMM-P,RatesFX,Interest Rate,Delta,JPY,,2023872525.630011'''
        ir7 = Sensitivity('RatesFx', 'Risk_IRCurve', 'JPY', '2', '10y', 'Libor3m', 90000000, 'USD', 90000000)
        ir8 = Sensitivity('RatesFx', 'Risk_IRCurve', 'JPY', '2', '20y', 'Libor3m', 10000000, 'USD', 10000000)
        tree = Simm.calculateTreeStandard(Arrays.asList(ir7.getJavaObj(), ir8.getJavaObj()), 'USD')
        treeString = GenerateCsvString.parseToFlatCsv(tree)
        self.assertEqual(treeRes, treeString)