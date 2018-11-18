import unittest

from simmLib.simmLib import *

class simmUnitTests(unittest.TestCase):

    def testNettingAndAbsoluteNotional(self):
        notional1 = ScheduleNotional('trade1', 'Rates', '2018-09-12', '2018-11-23', 1000, 'USD', 1000)
        notional2 = ScheduleNotional("trade2", "Rates", "2018-09-12", "2018-11-23", "-1000", "USD", "-1000")
        pv1a = SchedulePv("trade1", "Rates", "2018-09-12", "2018-11-23", "2000", "USD", "2000")
        pv1b = SchedulePv("trade1", "Rates", "2018-09-12", "2018-11-23", "-1000", "USD", "-1000")
        pv2 = SchedulePv("trade2", "Rates", "2018-09-12", "2018-11-23", "-1000", "USD", "-1000")
        self.assertEqual(8, Schedule.calculate(Arrays.asList(notional1.getJavaObj(), notional2.getJavaObj()), Arrays.asList(pv1a.getJavaObj(), pv1b.getJavaObj(), pv2.getJavaObj())).doubleValue())

    def testIR7(self):
        ir7 = Sensitivity('RatesFx', 'Risk_IRCurve', 'JPY', '2', '10y', 'Libor3m', 90000000, 'USD', 90000000)
        ir8 = Sensitivity('RatesFx', 'Risk_IRCurve', 'JPY', '2', '20y', 'Libor3m', 10000000, 'USD', 10000000)
        val = Simm.calculateStandard(Arrays.asList(ir7.getJavaObj(), ir8.getJavaObj()), 'USD').doubleValue()
        self.assertEqual(2023872526, round(val))