from simmLib.simmLib import *

def JavaArrayListToPythonList(Array):
    result = []
    for i in Array:
        result.append(i)
    return result

def JavaArrayListOfJavaSensitivitiesToListOfSensitivities(Array):
    result = []
    for i in Array:
        result.append(Sensitivity(i))
    return result