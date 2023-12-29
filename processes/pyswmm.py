import pywps
from pywps import Process, ComplexInput, ComplexOutput, Format, FORMATS

__author__ = 'Mingda Zhang'


class SWMM(Process):
    def __init__(self):
        inputs = [ComplexInput('inp_in', 'INP file',
                               # supported_formats=[Format('application/json')]
                               supported_formats=[Format('text/plain')]
                               )]
        outputs = [ComplexOutput('swmm_out', 'Buffered file',
                                 supported_formats=[FORMATS.JSON]
                                 )]

        super(SWMM, self).__init__(
            self._handler,
            identifier='swmm',
            version='1.0',
            title="swmm",
            abstract="pyswmm",
            profile='',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        from pyswmm import Simulation
        inp = request.inputs['inp_in'][0].file

        sim = Simulation(inp)
        sim.execute()

        outf = inp.replace(".inp", ".out")
        csvf = inp.replace(".inp", ".csv")

        import swmm_api
        from swmm_api import read_out_file
        out = read_out_file(outf)  # type: swmm_api.SwmmOut
        df = out.to_frame()  # type: pandas.DataFrame
        # print(df)
        output_path = pywps.configuration.get_config_value("server", "outputpath")
        df.to_csv(f'{output_path}/{csvf.split("/")[-1]}')
        output_url = pywps.configuration.get_config_value("server", "outputurl")

        response.outputs['swmm_out'].data = output_url + csvf.split('/')[-1]

        return response
