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
        # After the creation the CRIF consists of ArrayLists of Java objects (sensitivitities, scheduleNotionals etc)
        print(str(crif.getAllSensitivities()))
        print(str(crif.getAllAddonNotionals()))
        # The data set used for creating the crif is stored within the crif object:
        print(str(crif.asDataFrame.head(20)))
        asdf = 1

    def test_sample_multiCrifImport(self):
        csvLocation = 'test/UnitTest_CRIF.txt'
        # Use the Crifs class to create a dictionary of crifs of different counterparties, directions and regulations:
        crifs = Crifs(CRIF.CrifUtil.read_csv(csvLocation, sep='\t'))
        # A Crifs object may be used as any other python Dictionary. The key is a concatenated String of the Form
        # counterparty_direction_regulation and the values are the associated Crif Objects.
