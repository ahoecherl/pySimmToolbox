import unittest
from Calculation.StandardCalculation import StandardCalculation
from Calculation.StandaloneAllocation import StandaloneAllocation
from CRIF.Crif import Crif
import pandas as pd
import time
import CRIF

class StandardAllocationTest(unittest.TestCase):

    def test_performance_SA(self):
        Input = CRIF.CrifUtil.read_csv(r'../NochKleineresTestportfolio.csv')
        tic = time.time()
        crif = Crif(Input)
        imTree = StandardCalculation.calculate(crif)
        imTree = StandaloneAllocation.calculate(imTree)
        toc = time.time()
        self.assertTrue((toc-tic) < 0.8)