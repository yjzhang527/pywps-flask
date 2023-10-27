from pywps import Process, LiteralInput, ComplexOutput, FORMATS, Format
from pywps.app.Common import Metadata
from pywps.inout.outputs import MetaLink4, MetaFile


class TestJson(Process):
    def __init__(self):
        inputs = [LiteralInput('name', 'Input name', data_type='string')]
        outputs = [ComplexOutput('out', 'Referenced Output',
                                 supported_formats=[FORMATS.JSON])]

        super(TestJson, self).__init__(
            self._handler,
            identifier='testjson',
            title='Process Test.py',
            version='1.0.0',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        # data = json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
        # out_bytes = json.dumps(data, indent=2)
        # response.outputs['out'].output_format = 'application/json'
        # response.outputs['out'].data = out_bytes

        response.outputs['out'].output_format = Format('application/json')
        response.outputs['out'].data = {'out_bytes': '111'}
        return response
