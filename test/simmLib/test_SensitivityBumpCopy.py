import unittest
from simmLib.simmLib import *
from simmLib.simmLibUtils import *

class sensitivityCopyTest(unittest.TestCase):

    def test1(self):
        sensitivity1 = createSensitivity('RatesFX', 'Risk_FX', 'CHF', '', '', '', 12, 'USD', 12)
        sensitivity2 = createSensitivity(sensitivity1.bump(BigDecimal('0.1')))
        self.assertEqual(12, getSensitivityAmount(sensitivity1))
        self.assertEqual(13.2, getSensitivityAmount(sensitivity2))