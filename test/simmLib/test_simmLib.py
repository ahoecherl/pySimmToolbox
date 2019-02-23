import unittest
from simmLib.simmLib import *
from simmLib.simmLibUtils import *

class simmLibTest(unittest.TestCase):

    def test_Sensitivity(self):
        sensitivity = createSensitivity('RatesFX', 'Risk_FX', 'CHF', '', '', '', 12, 'USD', 12)
        self.assertEqual('Risk_FX', sensitivity.getRiskType())
        self.assertAlmostEqual(12, getSensitivityAmount(sensitivity))

    def test_ProductMultiplier(self):
        productMultiplier = createProductMultiplier('RatesFX', 1.205)
        self.assertEqual('RatesFX', getProductMultiplierProductClass(productMultiplier))
        self.assertAlmostEqual(1.205, getProductMultiplierMultiplier(productMultiplier))

    def test_AddOnNotionalFactor(self):
        addOnNotionalFactor = createAddOnNotionalFactor('ProductOne', 6.105)
        self.assertEqual('ProductOne', addOnNotionalFactor.getProduct())
        self.assertAlmostEqual(6.105, getAddOnNotionalFactorFactor(addOnNotionalFactor))

    def test_AddOnFixedAmount(self):
        addOnFixedAmount = createAddOnFixedAmount(130, 'EUR', 150)
        self.assertEqual('EUR', addOnFixedAmount.getCurrency())
        self.assertAlmostEqual(150, getAddOnFixedAmountAmountUsd(addOnFixedAmount))

    def test_AddOnNotional(self):
        addOnNotional = createAddOnNotional('ProductOne', 180, 'EUR', 210)
        self.assertEqual(addOnNotional.getProduct(), 'ProductOne')
        self.assertAlmostEqual(getAddOnNotionalNotionalUsd(addOnNotional), 210)

    def test_ScheduleNotional(self):
        scheduleNotional = createScheduleNotional('trade1', 'Rates', '2018-09-12', '2018-11-23', 1000, 'EUR', 1200)
        self.assertEqual('2018-11-23', getScheduleNotionalEndDate(scheduleNotional))
        self.assertAlmostEqual(1200, getScheduleNotionalAmountUsd(scheduleNotional))
        self.assertEqual('2018-09-12', getScheduleNotionalValuationDate(scheduleNotional))
        self.assertEqual('trade1', scheduleNotional.getTradeId())
        self.assertAlmostEqual(1000, scheduleNotional.getAmount().doubleValue(), places=3)
        self.assertEqual('Rates', scheduleNotional.getProductClass().getLabel())

    def test_SchedulePv(self):
        schedulePv = createSchedulePv('trade1', 'Rates', '2018-09-12', '2018-11-23', 1000, 'EUR', 1200)
        self.assertEqual('2018-11-23', getSchedulePvEndDate(schedulePv))
        self.assertAlmostEqual(1200, getSchedulePvAmountUsd(schedulePv))
        self.assertEqual('2018-09-12', getSchedulePvValuationDate(schedulePv))
        self.assertEqual('trade1', schedulePv.getTradeId())
        self.assertAlmostEqual(1000, schedulePv.getAmount().doubleValue(), places=3)
        self.assertEqual('Rates', schedulePv.getProductClass().getLabel())

    def testIR7tree(self):
        treeRes = '''Level,Im Model,Silo,RiskClass,SensitivityType,Bucket,WeightedSensitivity,ExposureAmount
1.Total,Total,,,,,,2023872525.630011
2.ImModel,SIMM-P,,,,,,2023872525.630011
3.Silo,SIMM-P,RatesFX,,,,,2023872525.630011
4.Risk Class,SIMM-P,RatesFX,Interest Rate,,,,2023872525.630011
5.Sensitivity Type,SIMM-P,RatesFX,Interest Rate,Delta,,,2023872525.630011
6.Bucket,SIMM-P,RatesFX,Interest Rate,Delta,JPY,,2023872525.630011'''
        ir7 = createSensitivity('RatesFx', 'Risk_IRCurve', 'JPY', '2', '10y', 'Libor3m', 90000000, 'USD', 90000000)
        ir8 = createSensitivity('RatesFx', 'Risk_IRCurve', 'JPY', '2', '20y', 'Libor3m', 10000000, 'USD', 10000000)
        tree = Simm.calculateTreeStandard(Arrays.asList(ir7, ir8), 'USD')
        treeString = GenerateCsvString.parseToFlatCsv(tree)
        self.assertEqual(treeRes, treeString)