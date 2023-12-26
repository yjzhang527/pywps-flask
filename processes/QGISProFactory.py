import json
import os

from pywps import LiteralInput, LiteralOutput, ComplexInput, ComplexOutput, Format, BoundingBoxInput
from pywps.validator.mode import MODE

from .QGISProcess import QGISProcess


class QGISProcFactory():
    def InitAlgorithms(self):
        classList = []  # 实例列表
        for filenames in os.listdir(r'data'):
            # print(filenames)
            with open(f'data/{filenames}', 'r', encoding='utf8') as fp:
                json_data = json.load(fp)
                inputs = []
                for i in json_data.get('Input'):
                    if i:
                        if i[3].get('Parameter type') in [
                            'ParameterHeatmapPixelSize',
                            'QgsProcessingParameterNumber',
                            'QgsProcessingParameterDistance',
                            'ParameterPixelSize',
                            'QgsProcessingParameterDuration',
                            'QgsProcessingParameterScale',
                            'QgsProcessingParameterBand'
                        ]:
                            inputs.append(LiteralInput(i[0].get('Title'), i[1].get('Abstract'), data_type='float'))
                        elif i[3].get('Parameter type') == 'QgsProcessingParameterEnum':
                            inputs.append(LiteralInput(i[0].get('Title'), i[1].get('Abstract'), data_type='float',
                                                       abstract=json.dumps(i[4].get('Available values'))))
                        elif i[3].get('Parameter type') in [
                            'QgsProcessingParameterMultipleLayers',
                            'QgsProcessingParameterMapLayer'
                        ]:
                            inputs.append(ComplexInput(i[0].get('Title'), i[1].get('Abstract'),
                                                       max_occurs=2,
                                                       supported_formats=[Format('image/tiff'),
                                                                          Format('application/zip'),
                                                                          Format('application/geo+json'),
                                                                          Format('application/json')], mode=MODE.NONE))
                        elif i[3].get('Parameter type') in [
                            'QgsProcessingParameterVectorLayer',
                            'QgsProcessingParameterFeatureSource',
                            'QgsProcessingParameterDxfLayers',
                            'QgsProcessingParameterVectorDestination',
                            'QgsProcessingParameterFeatureSink',
                        ]:
                            inputs.append(ComplexInput(i[0].get('Title'), i[1].get('Abstract'),
                                                       max_occurs=2,
                                                       supported_formats=[Format('application/zip')], mode=MODE.NONE))
                        elif i[3].get('Parameter type') in [
                            'QgsProcessingParameterRasterLayer',
                            'QgsProcessingParameterMeshLayer',
                            'QgsProcessingParameterRasterDestination',
                            'ParameterVrtDestination',
                            'ParameterVectorVrtDestination',
                        ]:
                            inputs.append(ComplexInput(i[0].get('Title'), i[1].get('Abstract'),
                                                       max_occurs=2,
                                                       supported_formats=[Format('image/tiff')], mode=MODE.NONE))
                        else:
                            inputs.append(LiteralInput(i[0].get('Title'), i[1].get('Abstract'), data_type='string'))

                outputs = []
                if type(json_data.get('Outputs')[0]) == dict:
                    json_data['Outputs'] = [json_data.get('Outputs')]
                for s in json_data.get('Outputs'):
                    if s[2].get('Parameter type') in [
                        'QgsProcessingOutputMultipleLayers',
                        'QgsProcessingOutputMapLayer'
                    ]:
                        outputs.append(ComplexOutput(s[0].get('Title'), s[1].get('Abstract'),
                                                     supported_formats=[Format('image/tiff'),
                                                                        Format('application/zip')]))
                    elif s[2].get('Parameter type') == 'QgsProcessingOutputVectorLayer':
                        outputs.append(ComplexOutput(s[0].get('Title'), s[1].get('Abstract'),
                                                     supported_formats=[Format('application/zip')]))
                    elif s[2].get('Parameter type') == 'QgsProcessingOutputRasterLayer':
                        outputs.append(ComplexOutput(s[0].get('Title'), s[1].get('Abstract'),
                                                     supported_formats=[Format('image/tiff')]))
                    elif s[2].get('Parameter type') == 'QgsProcessingOutputNumber':
                        outputs.append(LiteralOutput(s[0].get('Title'), s[1].get('Abstract'), data_type='float'))
                    else:
                        outputs.append(LiteralOutput(s[0].get('Title'), s[1].get('Abstract'), data_type='string'))

                identifier = json_data.get('Identifier')
                title = json_data.get('Title')
                abstract = json_data.get('Abstract')
                classList.append(QGISProcess(identifier, title, abstract, inputs, outputs))

        return classList


if __name__ == '__main__':
    cls = QGISProcFactory()
    cls.InitAlgorithms()
