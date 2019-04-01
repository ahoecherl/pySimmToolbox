from simmLib.simmLib import ArrayList, BigDecimal
from CRIF.Crif import Crif

class BumpedCrif(Crif):

    def __init__(self, CRIF, tradeId, eps):

        if CRIF.Sensitivities:
            self.Sensitivities = CRIF.Sensitivities.copy() #Shallow copy of the dict
            if tradeId in self.Sensitivities:
                newList = ArrayList()
                for s in self.Sensitivities[tradeId]:
                    newList.add(s.bump(BigDecimal(str(eps))))
                self.Sensitivities[tradeId] = newList

        if CRIF.AddOnNotionals:
            self.AddOnNotionals = CRIF.AddOnNotionals.copy()
            if tradeId in self.AddOnNotionals:
                newList = ArrayList()
                for n in self.AddOnNotionals[tradeId]:
                    newList.add(n.bump(BigDecimal(str(eps))))
                self.AddOnNotionals[tradeId] = newList

        if CRIF.ScheduleNotionals:
            self.ScheduleNotionals = CRIF.ScheduleNotionals.copy()
            if tradeId in self.ScheduleNotionals:
                newList = ArrayList()
                for n in self.ScheduleNotionals[tradeId]:
                    newList.add(n.bump(BigDecimal(str(eps))))
                self.ScheduleNotionals[tradeId] = newList

        if CRIF.SchedulePVs:
            self.SchedulePVs = CRIF.SchedulePVs.copy()
            if tradeId in self.SchedulePVs:
                newList = ArrayList()
                for p in self.SchedulePVs[tradeId]:
                    newList.add(p.bump(BigDecimal(str(eps))))
                self.SchedulePVs[tradeId] = newList