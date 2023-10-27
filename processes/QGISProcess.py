from qgis.core import *

from pywps import Process

QgsApplication.setPrefixPath(r'C:\Program Files\QGIS 3.32.1', True)
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
        body = {i[0]: i[1][0].data for i in request.inputs.items()}
        # print(body)
        ret = processing.run(self.identifier, body)

        # response.outputs[request.outputs[0]].data = 'success data in %s!'
        response.outputs['OUTPUT'].data = ret

        return response