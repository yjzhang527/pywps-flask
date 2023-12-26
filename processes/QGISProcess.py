import json

from qgis.core import *

from pywps import Process

QgsApplication.setPrefixPath(r'C:\OSGeo4W', True)
qgs = QgsApplication([], True)
qgs.initQgis()
print('qgs initialized')

from processing.core.Processing import Processing

Processing().initialize()
print('algorithm initialized')


class QGISProcess(Process):
    def __init__(self, identifier, title, abstract, inputs, outputs):
        '''
        inputs = [LiteralInput('name', 'Input name', data_type='string')]
        outputs = [LiteralOutput('response',
                                 'Output response', data_type='string')]
        '''
        super(QGISProcess, self).__init__(
            self._handler,
            identifier=str(identifier),
            title=str(title),
            abstract=str(abstract),
            version='1.3.3.7',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        from processing.core.Processing import processing

        body = {}
        for key, value in request.inputs.items():
            if len(value) > 1:
                body[key] = [i.data for i in value]
            else:
                body[key] = value[0].data

        # body = {i[0]: i[1][0].data for i in request.inputs.items()}
        # print(request.inputs)
        # print(body)
        print(json.loads(request.http_request.data))
        ret = processing.run(self.identifier, body)

        # response.outputs['BASIN'].data = ret['BASIN']
        for key, value in ret.items():
            if key in response.outputs and hasattr(response.outputs[key], "data"):
                response.outputs[key].data = value
