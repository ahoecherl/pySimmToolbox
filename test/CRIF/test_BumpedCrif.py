import unittest
from CRIF.Crif import Crif
from CRIF.BumpedCrif import BumpedCrif
import pandas as pd
from test.testUtils import *
from simmLib.simmLib import Simm
import CRIF.CrifUtil

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
        autoSensis = JavaArrayListOfJavaSensitivitiesToListOfSensitivities(bumpedCrif.Sensitivities[tradeId])
        manuellSensis = JavaArrayListOfJavaSensitivitiesToListOfSensitivities(manuelCrif.Sensitivities[tradeId])
        for i in range(0, len(autoSensis)):
            self.assertAlmostEqual(autoSensis[i].getAmount(), manuellSensis[i].getAmount(), places = 5)
        self.assertAlmostEqual(resultAutoBumped, resultManBumped, places = 3)
        self.assertNotAlmostEqual(resultOrig, resultManBumped, places = 0)
        self.assertNotAlmostEqual(resultOrig, resultAutoBumped, places = 0)