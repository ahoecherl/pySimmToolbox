import unittest
from CRIF.Crif import Crif
from CRIF import CrifUtil
import pandas as pd
from simmLib.simmLib import *
from CRIF.Crifs import Crifs
from testUtils import *

class CrifTest(unittest.TestCase):

    def test1(self):
        Input = CrifUtil.read_csv(r'../NochKleineresTestportfolio.csv')
        crif = Crif(Input)
        self.assertEqual('IMLedis_NRW_Bank', crif.Counterparty)
        self.assertEqual('collect', crif.direction)
        self.assertEqual('EMIR', crif.regulation)
        del crif

    def test2(self):
        Input = CrifUtil.read_csv(r'../Testdatensatz1_CRIF.csv')
        self.assertRaises(ValueError, Crif, Input)

    def test3(self):
        Input = CrifUtil.read_csv(r'../NochKleineresTestportfolio.csv')
        crif = Crif(Input)
        self.assertEqual(True, crif.asDataFrame.equals(Input))
        del crif

    def test5(self):
        Input = CrifUtil.read_csv(r'../testIR11asCRIF.csv')
        crif1 = Crif(Input)
        crif2 = Crif(Input)
        self.assertEqual(31773442304, round(Simm.calculateStandard(crif1.getAllSensitivities(), 'USD').doubleValue()))
        self.assertEqual(31773442304, round(Simm.calculateStandard(crif2.getAllSensitivities(), 'USD').doubleValue()))

    def test7(self):
        Input = CrifUtil.read_csv(r'../Testdatensatz1_CRIF.csv')
        crifs = Crifs(Input)
        crif = crifs.values().__iter__().__next__()
        leArray = crif.getAllScheduleNotionals()
        value = leArray[0].getAmount().doubleValue()
        self.assertEqual(value, 140002181.4934)
        crif = crifs['CDS-10015292-18_collect_EMIR']
        leArray = crif.getAllScheduleNotionals()
        value = leArray[3].getAmountUSD().doubleValue()
        self.assertEqual(value, 18000000)

    def test8(self):
        Input = CrifUtil.read_csv(r'../Testdatensatz1_CRIF.csv')
        crifs = Crifs(Input)
        crif = crifs['CDS-10015292-18_collect_EMIR']
        leArray = crif.getAllSchedulePVs()
        value = leArray[0].getAmountUSD().doubleValue()
        self.assertEqual(value, 4831209.57108)

    def test9(self):
        Input = CrifUtil.read_csv(r'../Unittest_CRIF.txt', sep = '\t')
        crifs = Crifs(Input)
        crif = crifs['testAN1_collect_EMIR']
        notionals = crif.getAllAddonNotionals()
        factors = crif.getAllAddOnNotionalFactors()
        notionals = JavaArrayListToPythonList(notionals)
        factors = JavaArrayListToPythonList(factors)
        self.assertEqual(notionals[0].getNotional().doubleValue(), 10000000.0)
        self.assertEqual(factors[0].getFactor().doubleValue(), 6.105)