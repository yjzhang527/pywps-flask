import processing
from qgis.core import *


QgsApplication.setPrefixPath(r'E:\QGIS', True)

qgs = QgsApplication([], True)

qgs.initQgis()
# print('qgs initialized')
#
#
import processing
# import sys
# import preprocess
# sys.path.append(r"E:\QGIS\apps\qgis-ltr\python\plugins")
from processing.core.Processing import Processing
Processing().initialize()
print('algorithm initialized')

# from qgis.analysis import QgsNativeAlgorithms
# QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
# for alg in QgsApplication.processingRegistry().algorithms():
#     print("{}:{} --> {}".format(alg.provider().name(), alg.name(), alg.displayName()))

import sys
f=open("myprint2.txt","w+",encoding="utf-8")
sys.stdout = f
for alg in QgsApplication.processingRegistry().algorithms():
    print("===========================================")
    processing.algorithmHelp(alg.id())



