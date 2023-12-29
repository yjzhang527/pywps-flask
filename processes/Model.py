"""
Model exported as python.
Name : model
Group :
With QGIS : 32813
"""
from processing.tools import dataobjects

from qgis.core import *
from scipy.odr import Model


class Model(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        pass

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Fill Sinks XXL (Wang & Liu)
        alg_params = {
            'ELEV': 'ASTGTM2_N05W058_dem_75179b25_806b_407a_9bb3_b1da3afcb689',
            'MINSLOPE': 1,
            'FILLED': QgsProcessing.TEMPORARY_OUTPUT
        }

        from processing.core.Processing import processing
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
        return results

    def name(self):
        return 'model'

    def displayName(self):
        return 'model'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model()


if __name__ == '__main__':
    cls = Model()
    feedback = QgsProcessingFeedback()
    context = dataobjects.createContext(feedback)

    cls.processAlgorithm(parameters=None, context=context, model_feedback=feedback)
