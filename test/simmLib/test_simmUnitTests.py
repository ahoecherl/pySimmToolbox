import unittest
import CRIF.CrifUtil
from CRIF.Crifs import Crifs
from CRIF.Crif import Crif
from Calculation.StandardCalculation import StandardCalculation

from simmLib.simmLib import *

class simmUnitTests(unittest.TestCase):

    def testNettingAndAbsoluteNotional(self):
        crifs = Crifs(CRIF.CrifUtil.read_csv('..\ScheduleTestSet.csv'))
        crif = crifs['Contract_3_collect_EMIR']
        imTree = StandardCalculation.calculate(crif)
        self.assertEqual(8, imTree.getMargin())