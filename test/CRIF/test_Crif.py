import unittest
from CRIF.Crif import Crif
from CRIF import CrifUtil
import pandas as pd
from simmLib.simmLib import Simm

class CrifTest(unittest.TestCase):

    def test1(self):
        Input = pd.read_csv(r'../NochKleineresTestportfolio.csv')
        crif = Crif(Input)
        self.assertEqual('IMLedis_NRW_Bank', crif.Counterparty)
        self.assertEqual('collect', crif.direction)
        self.assertEqual('EMIR', crif.regulation)
        del crif

    def test2(self):
        Input = pd.read_csv(r'../Testdatensatz1_CRIF.csv')
        self.assertRaises(ValueError, Crif, Input)

    def test3(self):
        Input = pd.read_csv(r'../NochKleineresTestportfolio.csv')
        crif = Crif(Input)
        self.assertEqual(True, crif.asDataFrame.equals(Input))
        del crif

    def test4(self):
        Input = pd.read_csv(r'../NochKleineresTestportfolio.csv')
        crif = Crif(Input)
        self.assertEqual(5203178, round(Simm.calculateStandard(crif.getAllSensitivities(), 'USD').doubleValue()))
        del crif

    def test5(self):
        Input = CrifUtil.read_csv(r'../testIR11asCRIF.csv')
        crif1 = Crif(Input)
        crif2 = Crif(Input)
        self.assertEqual(31773442304, round(Simm.calculateStandard(crif1.getAllSensitivities(), 'USD').doubleValue()))
        self.assertEqual(31773442304, round(Simm.calculateStandard(crif2.getAllSensitivities(), 'USD').doubleValue()))