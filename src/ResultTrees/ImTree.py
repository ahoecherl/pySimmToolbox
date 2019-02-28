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

    def toDataFrame(self):
        result = pd.DataFrame(columns=['Level','Total','Im Model', 'Silo', 'RiskClass', 'SensitivityType', 'Bucket', 'WeightedSensisitvity', 'AllocationType', 'tradeID', 'ExposureAmount','identifier','parentIdentifier'])
        lastLevel = {}
        for nodekey, node in self.nodes.items():
            Level = node.data.Level
            columnName = result.columns[Level]
            series = pd.Series({'Level': node.data.Level,
                                'ExposureAmount': node.data.ExposureAmount,
                                columnName: node.data.manifestation})
            if Level-1 in lastLevel:
                series = series.append(lastLevel[Level-1])
            series.at['AllocationType'] = 'None'
            series.at['identifier'] = str(node.identifier)
            if node.bpointer is not None:
                series.at['parentIdentifier'] = str(self.get_node(node.bpointer).identifier)
            lastLevel[Level] = series[result.columns[1:(Level + 1)]]
            result = result.append(series, ignore_index=True)
            if self.hasEulerAllocation:
                seriesBase = series.drop(['ExposureAmount', 'AllocationType'])
                for key, value in node.data.eulerAllocation.items():
                    seriesBase.at['ExposureAmount'] = value
                    seriesBase.at['AllocationType'] = 'Euler'
                    seriesBase.at['tradeID'] = key
                    result = result.append(seriesBase, ignore_index=True)
            if self.hasStandaloneAllocation:
                seriesBase = series.drop(['ExposureAmount', 'AllocationType'])
                for key, value in node.data.standaloneAllocation.items():
                    seriesBase.at['ExposureAmount'] = value
                    seriesBase.at['AllocationType'] = 'Standalone'
                    seriesBase.at['tradeID'] = key
                    result = result.append(seriesBase, ignore_index=True)
            asdf = 1
        result = result.fillna('')
        return result

    def printToCsv(self, path):
        result = self.toDataFrame()
        result.to_csv(path, index=False)

    def addScheduleTree(self, FlatTree):
        length = len(self._nodes)
        if isinstance(FlatTree, str):
            FlatTree = StringIO(FlatTree)
            FlatTree = ResultTrees.ImTreeUtil.read_csv(FlatTree)
        self.FlatTree = self.FlatTree.append(FlatTree.iloc[1:]).reset_index(drop=True)
        it = FlatTree.iterrows()
        i = 0
        data = ImNodeData(it.__next__()) # Throw Away root
        data = ImNodeData(it.__next__())
        self.create_node(tag = str(data), identifier=length, data=data, parent=0)
        self.get_node(0).data.ExposureAmount += data.ExposureAmount
        self.get_node(0).tag=str(self.get_node(0).data)
        for row in it:
            data=ImNodeData(row)
            i += 1
            node = Node(tag=str(data), identifier=i+length, data=data)
            parent_id = self.identify_parent_id(node)
            self.add_node(node, parent_id)

    def getMargin(self):
        return self._nodes[0].data.ExposureAmount

    def to_dict(self, nid=None, key=None, sort=True, reverse=False, with_data=False):
        """transform self into a dict"""

        nid = self.root if (nid is None) else nid
        ntag = self[nid].tag
        tree_dict = {ntag: {"children": []}}
        if with_data:
            tree_dict[ntag]["data"] = self[nid].data.to_dict()

        if self[nid].expanded:
            queue = [self[i] for i in self[nid].fpointer]
            key = (lambda x: x) if (key is None) else key
            if sort:
                queue.sort(key=key, reverse=reverse)

            for elem in queue:
                tree_dict[ntag]["children"].append(
                    self.to_dict(elem.identifier, with_data=with_data, sort=sort, reverse=reverse))
            if len(tree_dict[ntag]["children"]) == 0:
                tree_dict = self[nid].tag if not with_data else \
                            {ntag: {"data":self[nid].data.to_dict()}}
            return tree_dict