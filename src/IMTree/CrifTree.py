from treelib import Node
from treelib import Tree
from IMTree.CrifNodeData import CrifNodeData
from io import StringIO
import pandas as pd

class CrifTree(Tree):

    def identify_parent_id(self, node):
        refNode = self.leaves()[-1]
        while refNode.data.Level >= node.data.Level:
            refNode = self.get_node(refNode.bpointer)
        return refNode.identifier

    def __init__(self, CRIF):

        if isinstance(CRIF, str):
            CRIF = StringIO(CRIF)
            CRIF = pd.read_csv(CRIF, sep=',')
        super(CrifTree, self).__init__()
        it = CRIF.iterrows()
        data = CrifNodeData(it.__next__())
        i=0
        self.create_node(tag=str(data), identifier=i, data=data)
        while i<(CRIF.shape[0]-1):
            data = CrifNodeData(it.__next__())
            i = i+1
            node = Node(tag=str(data), identifier=i, data=data)
            parent_id = self.identify_parent_id(node)
            self.create_node(tag = str(data), identifier=i, data=data, parent=parent_id)