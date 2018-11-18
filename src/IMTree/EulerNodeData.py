from NodeData import NodeData

class EulerNodeData(NodeData):
    def __init__(self, origNodeData, bumpedNodeData, tradeID, eps, factor):
        if origNodeData.data.Level == 1:
            self.manifestation=tradeID
            self.levelName='Trade'
            self.value = (bumpedNodeData.data.value - origNodeData.data.value)/eps * factor
            self.Level = 2
        else:
            self.manifestation = origNodeData.data.manifestation
            self.levelName = origNodeData.data.levelName
            self.Level = origNodeData.data.Level+1
            self.value = (bumpedNodeData.data.value - origNodeData.data.value)/eps

