import os
import sys

from qgis.core import *

QgsApplication.setPrefixPath(r'C:\Program Files\QGIS 3.28.13', True)

qgs = QgsApplication([], True)

qgs.initQgis()

print('qgs initialized')

import processing
from processing.core.Processing import Processing

Processing().initialize()
print('algorithm initialized')

# self.identifier = identifier
#         self.handler = handler
#         self.title = title
#         self.abstract = abstract
#         self.keywords = keywords if keywords is not None else []
#         self.metadata = metadata if metadata is not None else []
#         self.profile = profile if profile is not None else []
#         self.version = version
#         self.inputs = inputs if inputs is not None else []
#         self.outputs = outputs if outputs is not None else []
classList = []
for alg in QgsApplication.processingRegistry().algorithms():
    if alg is not None:
        algJson = {}
        algJson['identifier'] = alg.id()
        algJson['title'] = alg.displayName()
        algJson['data_type'] = alg.id()
        algJson['workdir'] = alg.id()
        algJson['abstract'] = alg.id()
        algJson['keywords'] = alg.id()
        algJson['metadata'] = alg.id()
        algJson['uoms'] = alg.id()
        algJson['min_occurs'] = alg.id()
        algJson['max_occurs'] = alg.id()
        algJson['mode'] = alg.id()
        algJson['allowed_values'] = alg.id()
        algJson['default'] = alg.id()
        algJson['default_type'] = alg.id()
        algJson['translations'] = alg.id()

        processing.run("saga:channelnetworkanddrainagebasins", {
            'DEM': 'C:/Users/Zzz/AppData/Local/Temp/processing_iwWGWP/7ad7f05a828e4fe3b11557cd601d9557/FILLED.sdat',
            'DIRECTION': 'TEMPORARY_OUTPUT', 'CONNECTION': 'TEMPORARY_OUTPUT', 'ORDER': 'TEMPORARY_OUTPUT',
            'BASIN': 'TEMPORARY_OUTPUT', 'SEGMENTS': 'TEMPORARY_OUTPUT', 'BASINS': 'TEMPORARY_OUTPUT',
            'NODES': 'TEMPORARY_OUTPUT', 'THRESHOLD': 7})
