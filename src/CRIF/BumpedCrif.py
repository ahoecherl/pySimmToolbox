from simmLib.simmLib import ArrayList, BigDecimal
from CRIF.Crif import Crif

class BumpedCrif(Crif):

    def __init__(self, CRIF, tradeId, eps):
        self.Sensitivities = CRIF.Sensitivities.copy() #Shallow copy of the dict
        newList = ArrayList()
        for s in self.Sensitivities[tradeId]:
            newList.add(s.bump(BigDecimal(str(eps))))
        self.Sensitivities[tradeId] = newList
        asdf=1