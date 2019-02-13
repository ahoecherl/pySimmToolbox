from treelib import Node
from treelib import Tree
from ResultTrees.ImNodeData import ImNodeData
from io import StringIO
import CRIF.CrifUtil
import ResultTrees.ImTreeUtil
import pandas as pd

class ImTree(Tree):

    def identify_parent_id(self, node):
        refNode = self.leaves()[-1]
        while refNode.data.Level >= node.data.Level:
            refNode = self.get_node(refNode.bpointer)
        return refNode.identifier

    def __init__(self, FlatTree):
        self.hasEulerAllocation = False
        self.hasStandaloneAllocation = False
        #if it isn't a String it should be a pandas Dataframe
        if isinstance(FlatTree, str):
            FlatTree = StringIO(FlatTree)
            FlatTree = ResultTrees.ImTreeUtil.read_csv(FlatTree)
        self.FlatTree = FlatTree
        super(ImTree, self).__init__()
        it = FlatTree.iterrows()
        i = 0
        data = ImNodeData(it.__next__())
        self.create_node(tag=str(data), identifier=i, data=data)
        while i<(FlatTree.shape[0] - 1):
            i = i + 1
            data = ImNodeData(it.__next__())
            node = Node(tag=str(data), identifier=i, data=data)
            parent_id = self.identify_parent_id(node)
            self.create_node(tag = str(data), identifier=i, data=data, parent=parent_id)

    def printToCsv(self, path):
        result = pd.DataFrame(columns=['nodeIdentifier', 'valueType', 'trade', 'value'])
        for nodekey, node in self.nodes.items():
            result = result.append(pd.Series({'nodeIdentifier':node.data.identifier, 'valueType':'exposure','trade': '','value': node.data.ExposureAmount}),ignore_index=True)
            if self.hasEulerAllocation:
                for key, value in node.data.eulerAllocation.items():
                    result = result.append(pd.Series({'nodeIdentifier':node.data.identifier, 'valueType': 'eulerAllocation', 'trade': key, 'value':value}),ignore_index=True)
            if self.hasStandaloneAllocation:
                for key, value in node.data.standaloneAllocation.items():
                    result = result.append(pd.Series(
                        {'nodeIdentifier': node.data.identifier, 'valueType': 'standaloneAllocation', 'trade': key,
                         'value': value}), ignore_index=True)
        result.to_csv(path)
        asdf = 1