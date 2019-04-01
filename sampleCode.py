import CRIF.CrifUtil
from CRIF.Crif import Crif
from CRIF.Crifs import Crifs
from Calculation.StandardCalculation import StandardCalculation
from Calculation.StandaloneAllocation import StandaloneAllocation
from Calculation.EulerAllocation import EulerAllocation
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
        print('CRIFS: ' + str(crifs))
        for crifkey, crif in crifs.items():
            print('Selected CRIF: ' + str(crif))
        asdf = 1

    def test_calculate_initial_margin(self):
        # To streamline it is only possible to create an IM Tree from which the Overall Initial Margin may be extracted
        # afterwards.
        # The structure of the IM Tree has been adopted from the open source acadiasoft engine.
        csvLocation = 'test/NochKleineresTestportfolio.csv'
        crif = Crif(CRIF.CrifUtil.read_csv(csvLocation, sep=','))
        # call StandardCalculation.calculate(crif) to calculate the Initial Margin and create an IM Tree
        imTree = StandardCalculation.calculate(crif)
        imTree = EulerAllocation.calculate(imTree)
        imTree = StandaloneAllocation.calculate(imTree)
        # The resulting IM Tree can be displayed relatively conveniently with print
        print(imTree)
        # Alternatively it may be transformed into a DataFrame to simplify analysis of the result in Python
        imTree_asDataFrame = imTree.toDataFrame()
        print(imTree_asDataFrame.head(10))
        print(imTree_asDataFrame.columns)
        # If you want to analyse further outside of python you can save the imTree as a .csv File
        imTree.printToCsv('./ExampleTreeAsCsv.csv')
        # Finally, you can extract the overall Initial Margin as follows:
        im = imTree.getMargin()
        print('The initial Margin of ' + str(crif) + ' is '+ '{:,.2f}'.format(im) +' USD.')
        # By default the calculationCurrency and the currency in which the margin is returned is USD
        asdf = 1