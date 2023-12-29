import json
import tempfile

import numpy as np
from osgeo import gdal
from processing.core.Processing import processing
from processing.tools import dataobjects
from qgis._core import QgsProcessing, QgsProcessingFeedback, QgsProcessingMultiStepFeedback

from pywps import Process, FORMATS, ComplexOutput, LiteralInput, BoundingBoxInput, ComplexInput, Format


class ChannelNetworkAndDrainageBasins(Process):
    def __init__(self):
        inputs = [
            ComplexInput('input', 'INP file',
                         supported_formats=[FORMATS.JSON])
        ]
        outputs = [
            ComplexOutput('DIRECTION', 'Buffered file',
                          supported_formats=[FORMATS.JSON]),
            ComplexOutput('CONNECTION', 'Buffered file',
                          supported_formats=[FORMATS.JSON]),
            ComplexOutput('ORDER', 'Buffered file',
                          supported_formats=[FORMATS.JSON]),
            ComplexOutput('BASIN', 'Buffered file',
                          supported_formats=[FORMATS.JSON]),
            ComplexOutput('SEGMENTS', 'Buffered file',
                          supported_formats=[FORMATS.JSON]),
            ComplexOutput('BASINS', 'Buffered file',
                          supported_formats=[FORMATS.JSON]),
            ComplexOutput('NODES', 'Buffered file',
                          supported_formats=[FORMATS.JSON])
        ]
        super(ChannelNetworkAndDrainageBasins, self).__init__(
            self._handler,
            identifier='channelnetworkanddrainagebasins',
            version='1.0',
            title="channelnetworkanddrainagebasins",
            abstract="channelnetworkanddrainagebasins",
            profile='',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        model_feedback = QgsProcessingFeedback()

        context = dataobjects.createContext()
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        input_tiff = r'tests/data/ASTGTM2_N05W058_dem/ASTGTM2_N05W058_dem.tif'
        # output_tiff = r'tests/data/ASTGTM2_N05W058_dem/ASTGTM2_N05W058_dem_clip.tif'
        temp_output_tiff = tempfile.NamedTemporaryFile(suffix='.tif', delete=True).name
        cutline_geojson = json.dumps(request.inputs['input'][0].data)

        options = gdal.WarpOptions(
            cutlineDSName=cutline_geojson,
            cropToCutline=True,
            cutlineWhere=None,
            dstNodata=0  # 背景值设置无色
        )
        gdal.Warp(temp_output_tiff, input_tiff, options=options)

        # Fill Sinks XXL (Wang & Liu)
        alg_params = {
            'ELEV': temp_output_tiff,
            'MINSLOPE': 1,
            'FILLED': QgsProcessing.TEMPORARY_OUTPUT
        }

        outputs['FillSinksXxlWangLiu'] = processing.run('saga:fillsinksxxlwangliu', alg_params, context=context,
                                                        feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Channel Network and Drainage Basins
        alg_params = {
            'DEM': outputs['FillSinksXxlWangLiu']['FILLED'],
            'DIRECTION': 'TEMPORARY_OUTPUT',
            'THRESHOLD': 7,
            'BASIN': QgsProcessing.TEMPORARY_OUTPUT,
            'BASINS': QgsProcessing.TEMPORARY_OUTPUT,
            'CONNECTION': QgsProcessing.TEMPORARY_OUTPUT,
            'DIRECTION': QgsProcessing.TEMPORARY_OUTPUT,
            'NODES': QgsProcessing.TEMPORARY_OUTPUT,
            'ORDER': QgsProcessing.TEMPORARY_OUTPUT,
            'SEGMENTS': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ChannelNetworkAndDrainageBasins'] = processing.run('saga:channelnetworkanddrainagebasins', alg_params,
                                                                    context=context, feedback=feedback,
                                                                    is_child_algorithm=True)

        for key, val in outputs['ChannelNetworkAndDrainageBasins'].items():
            response.outputs[key].data = val