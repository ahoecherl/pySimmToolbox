from simmLib.simmLib import *
from simmLib.simmLibUtils import *

def JavaArrayListToPythonList(Array):
    result = []
    try:
        for i in Array:
            result.append(i)
    except:
        pass
    return result