from qgis.core import *

from pywps import Process

QgsApplication.setPrefixPath(r'C:\Program Files\QGIS 3.32.1', True)
qgs = QgsApplication([], True)
qgs.initQgis()
print('qgs initialized')

from processing.core.Processing import Processing

Processing().initialize()

from qgis.core import QgsApplication

for alg in QgsApplication.processingRegistry().algorithms():
    # if 'native:buffer' == alg.name():
        # alg
    # print("{}:{} --> {}".format(alg.provider().name(), alg.name(), alg.displayName()))
    # print("{}:{}".format(alg.provider().name(), alg.name()))
    print("{}".format(alg.id()))
