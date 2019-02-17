import unittest
import CRIF.CrifUtil
import CRIF.Crifs
import Calculation.StandardCalculation
from testUtils import *

class ISDA_SIMM_UnittestLoad(unittest.TestCase):

    def test_loadUnittestCrif(self):
        dataframe = CRIF.CrifUtil.read_csv('../Unittest_CRIF.txt', sep='\t')
        Crifs = CRIF.Crifs.Crifs(dataframe)
        asdf = 1

class ISDA_SIMM_Unittests(unittest.TestCase):

    def setUp(self):
        dataframe = CRIF.CrifUtil.read_csv('../Unittest_CRIF.txt', sep='\t')
        self.Testcases = CRIF.Crifs.Crifs(dataframe)

    def testAN1(self):
        target = 610500
        self.runUnittest('testAN1', target)

    def testAN2(self):
        target = 1526250
        self.runUnittest('testAN2', target)

    def testAN3(self):
        target = 2747250
        self.runUnittest('testAN3', target)

    def testAN4(self):
        target = 3363750
        self.runUnittest('testAN4', target)

    def testAN5(self):
        target = 3363750.00
        self.runUnittest('testAN5', target)

    def testAN6(self):
        target = 16500000.00
        self.runUnittest('testAN6', target)

    def testAN7(self):
        target = 36500000.00
        self.runUnittest('testAN7', target)

    def testAN8(self):
        target = 19863750.00
        self.runUnittest('testAN8', target)

    def testBC1(self):
        target = 38000000.00
        self.runUnittest('testBC1', target)

    def testBC2(self):
        target = 19000000.00
        self.runUnittest('testBC2', target)

    def testBC3(self):
        target = 86653332.00
        self.runUnittest('testBC3', target)

    def testBC4(self):
        target = 89421194.00
        self.runUnittest('testBC4', target)

    def testCM1(self):
        target = 570000000.00
        self.runUnittest('testCM1', target)

    def testCM10(self):
        target = 49085079199.00
        self.runUnittest('testCM10', target)

    def testCM11(self):
        target = 359638708.00
        self.runUnittest('testCM11', target)

    def testCM12(self):
        target = 49717717006.00
        self.runUnittest('testCM12', target)

    def testCM2(self):
        target = 2550000000.00
        self.runUnittest('testCM2', target)

    def testCM3(self):
        target = 1430000000.00
        self.runUnittest('testCM3', target)

    def testCM4(self):
        target = 49033642297.00
        self.runUnittest('testCM4', target)

    def testCM5(self):
        target = 350000000.00
        self.runUnittest('testCM5', target)

    def testCM6(self):
        target = 120000000.00
        self.runUnittest('testCM6', target)

    def testCM7(self):
        target = 966948809.00
        self.runUnittest('testCM7', target)

    def testCM8(self):
        target = 2310000000.00
        self.runUnittest('testCM8', target)

    def testCM9(self):
        target = 4816133304.00
        self.runUnittest('testCM9', target)

    def testCMV1(self):
        target = 5502933299.00
        self.runUnittest('testCMV1', target)

    def testCMV2(self):
        target = 193811031.00
        self.runUnittest('testCMV2', target)

    def testCMV3(self):
        target = 131560191.00
        self.runUnittest('testCMV3', target)

    def testCMV4(self):
        target = 5087508748.00
        self.runUnittest('testCMV4', target)

    def testCMV5(self):
        target = 5296449605.00
        self.runUnittest('testCMV5', target)

    def testCMV6(self):
        target = 10067405222.00
        self.runUnittest('testCMV6', target)

    def testCMV7(self):
        target = 11968925376.00
        self.runUnittest('testCMV7', target)

    def testCMV8(self):
        target = 12012068652.00
        self.runUnittest('testCMV8', target)

    def testCNQ1(self):
        target = 450000000.00
        self.runUnittest('testCNQ1', target)

    def testCNQ10(self):
        target = 47064785518.00
        self.runUnittest('testCNQ10', target)

    def testCNQ2(self):
        target = 5537710718.00
        self.runUnittest('testCNQ2', target)

    def testCNQ3(self):
        target = 8818163074.00
        self.runUnittest('testCNQ3', target)

    def testCNQ4(self):
        target = 1393084423.00
        self.runUnittest('testCNQ4', target)

    def testCNQ5(self):
        target = 2346606060.00
        self.runUnittest('testCNQ5', target)

    def testCNQ6(self):
        target = 793725393.00
        self.runUnittest('testCNQ6', target)

    def testCNQ7(self):
        target = 38459653665.00
        self.runUnittest('testCNQ7', target)

    def testCNQ8(self):
        target = 8453486855.00
        self.runUnittest('testCNQ8', target)

    def testCNQ9(self):
        target = 38611298664.00
        self.runUnittest('testCNQ9', target)

    def testCNQV1(self):
        target = 6210000.00
        self.runUnittest('testCNQV1', target)

    def testCNQV2(self):
        target = 6632694.00
        self.runUnittest('testCNQV2', target)

    def testCNQV3(self):
        target = 9990000.00
        self.runUnittest('testCNQV3', target)

    def testCNQV4(self):
        target = 14170743.00
        self.runUnittest('testCNQV4', target)

    def testCNQV5(self):
        target = 13658371.00
        self.runUnittest('testCNQV5', target)

    def testCNQV6(self):
        target = 19629425.00
        self.runUnittest('testCNQV6', target)

    def testCNQV7(self):
        target = 20898727.00
        self.runUnittest('testCNQV7', target)

    def testCQ1(self):
        target = 69000000.00
        self.runUnittest('testCQ1', target)

    def testCQ10(self):
        target = 1068608674.00
        self.runUnittest('testCQ10', target)

    def testCQ11(self):
        target = 321490608.00
        self.runUnittest('testCQ11', target)

    def testCQ12(self):
        target = 3378851292.00
        self.runUnittest('testCQ12', target)

    def testCQ13(self):
        target = 1306838776.00
        self.runUnittest('testCQ13', target)

    def testCQ14(self):
        target = 1902604112.00
        self.runUnittest('testCQ14', target)

    def testCQ15(self):
        target = 2830853081.00
        self.runUnittest('testCQ15', target)

    def testCQ16(self):
        target = 4757786546.00
        self.runUnittest('testCQ16', target)

    def testCQ2(self):
        target = 1860488987.00
        self.runUnittest('testCQ2', target)

    def testCQ3(self):
        target = 166000000.00
        self.runUnittest('testCQ3', target)

    def testCQ4(self):
        target = 8326914194.00
        self.runUnittest('testCQ4', target)

    def testCQ5(self):
        target = 1983434521.00
        self.runUnittest('testCQ5', target)

    def testCQ6(self):
        target = 290210424.00
        self.runUnittest('testCQ6', target)

    def testCQ7(self):
        target = 4200448321.00
        self.runUnittest('testCQ7', target)

    def testCQ8(self):
        target = 629565922.00
        self.runUnittest('testCQ8', target)

    def testCQ9(self):
        target = 1818416923.00
        self.runUnittest('testCQ9', target)

    def testCQV1(self):
        target = 53811725.00
        self.runUnittest('testCQV1', target)

    def testCQV2(self):
        target = 5908978.00
        self.runUnittest('testCQV2', target)

    def testCQV3(self):
        target = 13500000.00
        self.runUnittest('testCQV3', target)

    def testCQV4(self):
        target = 14287057.00
        self.runUnittest('testCQV4', target)

    def testCQV5(self):
        target = 54180306.00
        self.runUnittest('testCQV5', target)

    def testCQV6(self):
        target = 12354863.00
        self.runUnittest('testCQV6', target)

    def testCQV7(self):
        target = 57583035.00
        self.runUnittest('testCQV7', target)

    def testEQ1(self):
        target = 60000000.00
        self.runUnittest('testEQ1', target)

    def testEQ10(self):
        target = 208620708.00
        self.runUnittest('testEQ10', target)

    def testEQ11(self):
        target = 847874443.00
        self.runUnittest('testEQ11', target)

    def testEQ12(self):
        target = 895893444.00
        self.runUnittest('testEQ12', target)

    def testEQ2(self):
        target = 150000000.00
        self.runUnittest('testEQ2', target)

    def testEQ3(self):
        target = 210000000.00
        self.runUnittest('testEQ3', target)

    def testEQ4(self):
        target = 780734787.00
        self.runUnittest('testEQ4', target)

    def testEQ5(self):
        target = 19040000.00
        self.runUnittest('testEQ5', target)

    def testEQ6(self):
        target = 172336879.00
        self.runUnittest('testEQ6', target)

    def testEQ7(self):
        target = 212089604.00
        self.runUnittest('testEQ7', target)

    def testEQ8(self):
        target = 788071639.00
        self.runUnittest('testEQ8', target)

    def testEQ9(self):
        target = 31824073.00
        self.runUnittest('testEQ9', target)

    def testEQV1(self):
        target = 319360046.00
        self.runUnittest('testEQV1', target)

    def testEQV10(self):
        target = 1582952747.00
        self.runUnittest('testEQV10', target)

    def testEQV11(self):
        target = 7261782938.00
        self.runUnittest('testEQV11', target)

    def testEQV12(self):
        target = 18278596023.00
        self.runUnittest('testEQV12', target)

    def testEQV2(self):
        target = 1345791692.00
        self.runUnittest('testEQV2', target)

    def testEQV3(self):
        target = 264329313.00
        self.runUnittest('testEQV3', target)

    def testEQV4(self):
        target = 208036959.00
        self.runUnittest('testEQV4', target)

    def testEQV5(self):
        target = 5312157001.00
        self.runUnittest('testEQV5', target)

    def testEQV6(self):
        target = 17404399.00
        self.runUnittest('testEQV6', target)

    def testEQV7(self):
        target = 12048394168.00
        self.runUnittest('testEQV7', target)

    def testEQV8(self):
        target = 1545642629.00
        self.runUnittest('testEQV8', target)

    def testEQV9(self):
        target = 5678830191.00
        self.runUnittest('testEQV9', target)

    def testFX1(self):
        target = 0.00
        self.runUnittest('testFX1', target)

    def testFX2(self):
        target = 16200000000.00
        self.runUnittest('testFX2', target)

    def testFX3(self):
        target = 19304527966.00
        self.runUnittest('testFX3', target)

    def testFX4(self):
        target = 19758023687.00
        self.runUnittest('testFX4', target)

    def testFXV1(self):
        target = 197113249.00
        self.runUnittest('testFXV1', target)

    def testFXV2(self):
        target = 84002960.00
        self.runUnittest('testFXV2', target)

    def testFXV3(self):
        target = 546819143.00
        self.runUnittest('testFXV3', target)

    def testFXV4(self):
        target = 199496275.00
        self.runUnittest('testFXV4', target)

    def testFXV5(self):
        target = 466370454.00
        self.runUnittest('testFXV5', target)

    def testIR1(self):
        target = 14200000000.00
        self.runUnittest('testIR1', target)

    def testIR10(self):
        target = 31779941448.00
        self.runUnittest('testIR10', target)

    def testIR11(self):
        target = 31773442304.00
        self.runUnittest('testIR11', target)

    def testIR2(self):
        target = 18645566306.00
        self.runUnittest('testIR2', target)

    def testIR3(self):
        target = 1517893277.00
        self.runUnittest('testIR3', target)

    def testIR4(self):
        target = 230000000.00
        self.runUnittest('testIR4', target)

    def testIR5(self):
        target = 2349609897.00
        self.runUnittest('testIR5', target)

    def testIR6(self):
        target = 12866994210.00
        self.runUnittest('testIR6', target)

    def testIR7(self):
        target = 2023872526.00
        self.runUnittest('testIR7', target)

    def testIR8(self):
        target = 6221583400.00
        self.runUnittest('testIR8', target)

    def testIR9(self):
        target = 31531158315.00
        self.runUnittest('testIR9', target)

    def testIRV1(self):
        target = 296817050.00
        self.runUnittest('testIRV1', target)

    def testIRV2(self):
        target = 48000000.00
        self.runUnittest('testIRV2', target)

    def testIRV3(self):
        target = 14248000000.00
        self.runUnittest('testIRV3', target)

    def testIRV4(self):
        target = 176551066.00
        self.runUnittest('testIRV4', target)

    def testIRV5(self):
        target = 56000000.00
        self.runUnittest('testIRV5', target)

    def testIRV6(self):
        target = 22028345.00
        self.runUnittest('testIRV6', target)

    def testIRV7(self):
        target = 387969168.00
        self.runUnittest('testIRV7', target)

    def testIRV8(self):
        target = 483003521.00
        self.runUnittest('testIRV8', target)

    def testRisk1(self):
        target = 31103027174.00
        self.runUnittest('testRisk1', target)

    def testGlobal(self):
        target = 190371821528.00
        self.runUnittest('testGlobal', target)

    def runUnittest(self, TestCaseName, target):
        crif = self.Testcases.get(TestCaseName+'_collect_EMIR')
        result = Calculation.StandardCalculation.StandardCalculation.calculate(crif)
        self.assertEqual(round(result.get_node(0).data.ExposureAmount, 0), target)