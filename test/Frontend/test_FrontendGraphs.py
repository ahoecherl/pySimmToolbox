import unittest
import pandas as pd
from Frontend.FrontendGraphs import *

class FrontendDataFilteringTest(unittest.TestCase):

    def test_treeGraph(self):
        df = pd.read_csv(r'../ExampleTreeAsCsv.csv', dtype={'parentIdentifier': 'str'})
        df = df.fillna('')
        treeGraph = create_tree_graph(df)