import unittest
import CRIF.CrifUtil
from CRIF.Crifs import Crifs
from CRIF.Crif import Crif
from Calculation.StandardCalculation import StandardCalculation

from simmLib.simmLib import *

class simmUnitTests(unittest.TestCase):

    def testNettingAndAbsoluteNotional(self):
        crifs = Crifs(CRIF.CrifUtil.read_csv('..\ScheduleTestSet.csv'))
        crif = crifs['NettingAndAbsoluteNotional_collect_EMIR']
        imTree = StandardCalculation.calculate(crif)
        self.assertEqual(8, imTree.getMargin())

    def testNettingAsExpected(self):
        crifs = Crifs(CRIF.CrifUtil.read_csv('..\ScheduleTestSet.csv'))
        crif = crifs['NettingAsExpected_collect_EMIR']
        imTree = StandardCalculation.calculate(crif)
        self.assertEqual(0, imTree.getMargin())

    def testNettingsAsExpectedPv(self):
        crifs = Crifs(CRIF.CrifUtil.read_csv('..\ScheduleTestSet.csv'))
        crif = crifs['NettingsAsExpectedPv_collect_EMIR']
        imTree = StandardCalculation.calculate(crif)
        self.assertEqual(10, imTree.getMargin())