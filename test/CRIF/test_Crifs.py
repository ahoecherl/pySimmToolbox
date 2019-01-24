import unittest
import pandas as pd
from CRIF import CrifUtil
from CRIF.Crifs import Crifs

class CrifsTest(unittest.TestCase):

    def test1(self):
        Input = CrifUtil.read_csv(r'../Testdatensatz1_CRIF.csv')
        crifs = Crifs(Input)
        self.assertEqual('CDS-10005292-18_collect_EMIR', crifs.keys().__iter__().__next__())

    def test2(self):
        Input = CrifUtil.read_csv(r'../Testdatensatz1_CRIF.csv')
        crifs = Crifs(Input)
        self.assertEqual(crifs.__len__(), 8)
