import pandas as pd
import os
from treelib import Node
from treelib import Tree
from IMTree.EulerNodeData import EulerNodeData
import collections

class EulerTree(Tree):

    def __identify_parent_id__(self, node, tradeID, OrigTree, i):
        if node.data.Level == 2:
           return 0
        if node.data.Level == 3:
            tradeNodes = self.children(0)
            for trades in tradeNodes:
                if trades.data.manifestation == tradeID:
                    tradeRoot = trades.identifier
            return tradeRoot
        else:
            tradeNodes = self.children(0)
            for trades in tradeNodes:
                if trades.data.manifestation==tradeID:
                    tradeRoot = trades.identifier
        Nodes = self.subtree(tradeRoot)._nodes
        Nodes = collections.OrderedDict(sorted(Nodes.items()))
        targetManifestation = OrigTree.get_node(OrigTree.get_node(i)._bpointer).data.manifestation
        targetLevelName = OrigTree.get_node(OrigTree.get_node(i).bpointer).data.levelName
        for key in reversed(list(Nodes.keys())):
            if (Nodes[key].data.manifestation == targetManifestation and Nodes[key].data.levelName == targetLevelName):
                return Nodes[key].identifier

    def __init__(self, OrigTree, BumpedTrees, eps):
        self.eps=eps
        super(EulerTree, self).__init__()
        # Creating the root
        root = Node(tag=str(OrigTree.get_node(OrigTree.root).data), data=OrigTree.get_node(OrigTree.root).data, identifier=0)
        self.add_node(root)
        size = OrigTree._nodes.keys().__len__()
        for i in range(0, size-1):
            sum=0
            for key in BumpedTrees:
                bumpedTree = BumpedTrees[key]
                sum = sum+(bumpedTree.get_node(i).data.value-OrigTree.get_node(i).data.value)/self.eps
            if sum==0:
                factor=1
            else:
                factor = 1
                #factor = OrigTree.get_node(i).data.value/sum

            for tradeID in BumpedTrees:
                bumpedTree = BumpedTrees[tradeID]
                newNodeData = EulerNodeData(origNodeData = OrigTree.get_node(i), bumpedNodeData = bumpedTree.get_node(i), tradeID = tradeID, eps = self.eps, factor = factor)
                currentId = self._nodes.keys().__len__()
                newNode = Node(tag=str(newNodeData), data=newNodeData, identifier=currentId)
                parent_id = self.__identify_parent_id__(newNode, tradeID, OrigTree, i)
                self.add_node(newNode, parent=parent_id)

        while (self.check_if_0_leaf()):
            for leaf in self.leaves():
                if leaf.data.value == 0:
                    self.remove_node(leaf.identifier)
        asdf=1

    def check_if_0_leaf(self):
        for leaf in self.leaves():
            if leaf.data.value == 0:
                return True
        return False
