import unittest
import pandas as pd
from Frontend.FrontendDataFiltering import *

class FrontendDataFilteringTest(unittest.TestCase):

    def test_getIM(self):
        df = pd.read_csv(r'../ExampleTreeAsCsv.csv')
        value = getIM(df)
        self.assertAlmostEquals(value, 6243814.18674, places=0)