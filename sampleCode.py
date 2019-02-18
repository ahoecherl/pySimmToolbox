import CRIF.CrifUtil
from CRIF.Crif import Crif
from CRIF.Crifs import Crifs
from Calculation import StandardCalculation, StandaloneAllocation, EulerAllocation
from ResultTrees import ImTree
import unittest

# Importing a CRIF
class codeSamples(unittest.TestCase):

    def test_sample_crifImport(self):
        csvLocation = 'test/NochKleineresTestportfolio.csv'
        # CrifUtil.read_csv should align different formatting styles of the CRIF.
        crif = Crif(CRIF.CrifUtil.read_csv(csvLocation, sep=','))
        # nach der Erzeugung besteht das CRIF aus ArrayListen von Javaobjekten (Sensitivitäten, ScheduleNotionals etc.)
        str(crif.getAllSensitivities())
        str(crif.getAllAddonNotionals())
        # Außerdem wurde der Datensatz abgespeichert aus dem das CRIF erstellt wurde.
        crif.asDataFrame.head(20)
        asdf = 1