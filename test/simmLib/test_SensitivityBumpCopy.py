import unittest
from simmLib.simmLib import *

class sensitivityCopyTest(unittest.TestCase):

    def test1(self):
        sensitivity1 = Sensitivity('RatesFX', 'Risk_FX', 'CHF', '', '', '', 12, 'USD', 12)
        sensitivity2 = Sensitivity(sensitivity1.getJavaObj().bump(BigDecimal('0.1')))
        self.assertEqual(12, sensitivity1.getAmount())
        self.assertEqual(13.2, sensitivity2.getAmount())