import unittest
import CRIF.CrifUtil
from CRIF.Crifs import Crifs
from CRIF.Crif import Crif
from Calculation.StandardCalculation import StandardCalculation

class StandardCalculationTest(unittest.TestCase):

    def test_ScheduleOnly(self):
        df = CRIF.CrifUtil.read_csv('../ScheduleTestSet.csv')
        crif = Crifs(df)['Contract_1_collect_EMIR']
        imTree = StandardCalculation.calculate(crif)
        self.assertEqual(round(imTree.get_node(0).data.ExposureAmount,0), 50400)

    def test_ScheduleAndSimm(self):
        df = CRIF.CrifUtil.read_csv('../ScheduleTestSet.csv')
        crif = Crifs(df)['Contract_2_collect_EMIR']
        imTree = StandardCalculation.calculate(crif)
        self.assertEqual(round(imTree.get_node(0).data.ExposureAmount,0), 191915)
