import unittest
from Calculation.EulerAllocation import EulerAllocation
from Calculation.StandardCalculation import StandardCalculation
from Calculation.StandaloneAllocation import StandaloneAllocation
from CRIF.Crif import Crif
from CRIF.Crifs import Crifs
import CRIF.CrifUtil
import pandas as pd
import time

class EulerAllocationTest(unittest.TestCase):

    def test_performance_JPM_komplett(self):
        Input = CRIF.CrifUtil.read_csv(r'../NochKleineresTestportfolio.csv')
        tic = time.time()
        crif = Crif(Input)
        imTree = StandardCalculation.calculate(crif)
        imTree = EulerAllocation.calculate(imTree)
        toc = time.time()
        print(toc-tic)
        asfd = 1
        self.assertTrue((toc - tic) < 20)

    def test_both_allocations(self):
        Input = CRIF.CrifUtil.read_csv(r'../NochKleineresTestportfolio.csv')
        tic = time.time()
        crif = Crif(Input)
        imTree = StandardCalculation.calculate(crif)
        imTree = EulerAllocation.calculate(imTree)
        imTree = StandaloneAllocation.calculate(imTree)
        toc = time.time()
        print(toc - tic)
        asfd = 1
        self.assertTrue((toc - tic) < 40)