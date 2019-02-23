import unittest
from CRIF.Crif import Crif
from CRIF.BumpedCrif import BumpedCrif
import pandas as pd
from test.testUtils import *
from simmLib.simmLib import Simm
import CRIF.CrifUtil
from CRIF.Crifs import Crifs

class CrifTest(unittest.TestCase):

    def test_originalStaysTheSame(self):
        Input = CRIF.CrifUtil.read_csv(r'../NochKleineresTestportfolio.csv')
        crif = Crif(Input)
        simm = Simm()
        result = simm.calculateStandard(crif.getAllSensitivities(),'USD').doubleValue()
        tradeIds = crif.Sensitivities.keys()
        tradeId = next(iter(tradeIds))
        bumpedCrif = BumpedCrif(crif, tradeId, 0.01)
        result2 = simm.calculateStandard(crif.getAllSensitivities(),'USD').doubleValue()
        self.assertEqual(result, result2)

    def test_bumpWorked(self):
        eps = 0.1
        tradeId = 'DZ14788807'
        Input = CRIF.CrifUtil.read_csv(r'../NochKleineresTestportfolio.csv')
        crif = Crif(Input)
        simm = Simm()
        bumpedCrif = BumpedCrif(crif, tradeId, eps)
        InputManBump = pd.read_csv(r'../NochKleineresTestportfolioManualBump.csv')
        manuelCrif = Crif(InputManBump)
        resultAutoBumped = simm.calculateStandard(bumpedCrif.getAllSensitivities(),'USD').doubleValue()
        resultManBumped = simm.calculateStandard(manuelCrif.getAllSensitivities(), 'USD').doubleValue()
        resultOrig = simm.calculateStandard(crif.getAllSensitivities(), 'USD').doubleValue()
        autoSensis = bumpedCrif.Sensitivities[tradeId]
        manuellSensis = manuelCrif.Sensitivities[tradeId]
        for i in range(0, autoSensis.size()):
            self.assertAlmostEqual(getSensitivityAmount(autoSensis.get(i)), getSensitivityAmount(manuellSensis.get(i)), places=5)
        self.assertAlmostEqual(resultAutoBumped, resultManBumped, places=3)
        self.assertNotAlmostEqual(resultOrig, resultManBumped, places=0)
        self.assertNotAlmostEqual(resultOrig, resultAutoBumped, places=0)

    def test_bumpAddOnNotional(self):
        eps = 0.1
        tradeId = 'AN3'
        Input = CRIF.CrifUtil.read_csv(r'..\Unittest_CRIF.txt', sep = '\t')
        crifs = Crifs(Input)
        crif = crifs['testAN1_collect_EMIR']
        bumpedCrif = BumpedCrif(crif, tradeId, eps)
        notionals = bumpedCrif.getAllAddonNotionals()
        notionals = JavaArrayListToPythonList(notionals)
        origNotionals = crif.getAllAddonNotionals()
        origNotionals = JavaArrayListToPythonList(origNotionals)
        self.assertEqual(notionals[0].getNotionalUsd().doubleValue(),11000000)
        self.assertEqual(origNotionals[0].getNotionalUsd().doubleValue(), 10000000)

    def test_bumpScheduleNotional(self):
        eps = 0.1
        Input = CRIF.CrifUtil.read_csv(r'..\ScheduleTestSet.csv', sep=',')
        crifs = Crifs(Input)
        crif = crifs['Contract_1_collect_EMIR']
        bumpedCrif = BumpedCrif(crif, 'trd1', eps)
        origScheduleNotionals = crif.getAllScheduleNotionals()
        scheduleNotionals = bumpedCrif.getAllScheduleNotionals()
        self.assertEqual(origScheduleNotionals[0].getAmountUSD().doubleValue(),120000)
        self.assertEqual(origScheduleNotionals[1].getAmount().doubleValue(),300000)
        self.assertEqual(scheduleNotionals[0].getAmountUSD().doubleValue(),132000)
        self.assertEqual(scheduleNotionals[1].getAmount().doubleValue(),300000)

    def test_bumpSchedulePVs(self):
        eps = 0.1
        Input = CRIF.CrifUtil.read_csv(r'..\ScheduleTestSet.csv', sep=',')
        crifs = Crifs(Input)
        crif = crifs['Contract_1_collect_EMIR']
        bumpedCrif = BumpedCrif(crif, 'trd1', eps)
        origSchedulePVs = crif.getAllSchedulePVs()
        schedulePVs = bumpedCrif.getAllSchedulePVs()
        self.assertEqual(origSchedulePVs[0].getAmountUSD().doubleValue(), 2200)
        self.assertEqual(origSchedulePVs[1].getAmount().doubleValue(), -4000)
        self.assertEqual(schedulePVs[0].getAmountUSD().doubleValue(), 2420)
        self.assertEqual(schedulePVs[1].getAmount().doubleValue(), -4000)
