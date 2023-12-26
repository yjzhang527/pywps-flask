#!/usr/bin/env python3
import json
# Copyright (c) 2016 PyWPS Project Steering Committee
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import random

import flask

import pywps
from PyQt5.QtCore import QVariant
from flask import jsonify, request
from processing.algs import qgis
from qgis._core import QgsApplication
from qgis.core import QgsVectorLayer, QgsFeature, QgsField, QgsGeometry, QgsPointXY, QgsField, QgsProject

from processes.pyswmm import SWMM
from processes.jsonprocess import TestJson
from pywps import Service

from processes.QGISProFactory import QGISProcFactory

app = flask.Flask(__name__)

processes = QGISProcFactory().InitAlgorithms()
processes.append(SWMM())
processes.append(TestJson())

# For the process list on the home page
process_descriptor = {}
for process in processes:
    abstract = process.abstract
    identifier = process.identifier
    process_descriptor[identifier] = abstract

# This is, how you start PyWPS instance
service = Service(processes, ['pywps.cfg'])


@app.route("/")
def hello():
    server_url = pywps.configuration.get_config_value("server", "url")
    request_url = flask.request.url
    return flask.render_template('home.html', request_url=request_url,
                                 server_url=server_url,
                                 process_descriptor=process_descriptor)


@app.route('/<base_url>', methods=['GET', 'POST'])
@app.route('/<base_url>/<identifier>', methods=['GET', 'POST'])
def wps_handle(base_url='wps', identifier=None, output_ids=None):
    """
        This function parses the request URL and extracts the following:
            default operation, process identifier, output_ids, default mimetype
            info that cannot be terminated from the URL will be None (default)

            The url is expected to be in the following format, all the levels are optional.
            [base_url]/[identifier]/[output_ids]

        :param http_request: the request URL
        :return: dict with the extracted info listed:
            base_url - [wps|processes|jobs|api/api_level]
            default_mimetype - determinate by the base_url part:
                XML - if the base url == 'wps',
                JSON - if the base URL in ['api'|'jobs'|'processes']
            operation - also determinate by the base_url part:
                ['api'|'jobs'] -> 'execute'
                processes -> 'describeprocess' or 'getcapabilities'
                    'describeprocess' if identifier is present as the next item, 'getcapabilities' otherwise
            api - api level, only expected if base_url=='api'
            identifier - the process identifier
            output_ids - if exist then it selects raw output with the name output_ids
        """
    return service


@app.route('/outputs/' + '<path:filename>')
def outputfile(filename):
    targetfile = os.path.join('outputs', filename)
    if os.path.isfile(targetfile):
        file_ext = os.path.splitext(targetfile)[1]
        with open(targetfile, mode='rb') as f:
            file_bytes = f.read()
        mime_type = None
        if 'xml' in file_ext:
            mime_type = 'text/xml'
        return flask.Response(file_bytes, content_type=mime_type)
    else:
        flask.abort(404)


@app.route('/static/' + '<path:filename>')
def staticfile(filename):
    targetfile = os.path.join('static', filename)
    if os.path.isfile(targetfile):
        with open(targetfile, mode='rb') as f:
            file_bytes = f.read()
        mime_type = None
        return flask.Response(file_bytes, content_type=mime_type)
    else:
        flask.abort(404)


@app.route('/list-algorithms', methods=['GET'])
def list_algorithms():
    algorithms = QgsApplication.processingRegistry().algorithms()

    algorithm_names = [algorithm.id() for algorithm in algorithms]
    return jsonify(algorithm_names)


def generate_vector_name():
    """
       生成一个随机的矢量要素名称。

       Returns:
           vector_name (str): 随机生成的矢量名称。
    """
    vector_name = ""
    for i in range(6):
        vector_name += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    return vector_name


@app.route('/publish-features', methods=['POST'])
def publish_features():
    """
       接收POST请求，将vector_json_data保存到文件中
       :return: None
    """
    vector_json_data = json.loads(request.get_data())
    layer_name = generate_vector_name()
    with open(f"static/requests/temp_{layer_name}.json", "w") as file:
        json.dump(vector_json_data, file)
    return layer_name


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="""Script for starting an example PyWPS
                       instance with sample processes""",
        epilog="""Do not use this service in a production environment.
         It's intended to be running in test environment only!
        For more documentation, visit http://pywps.org/doc
        """
    )
    parser.add_argument('-d', '--daemon',
                        action='store_true', help="run in daemon mode")
    parser.add_argument('-a', '--all-addresses',
                        action='store_true', help="run flask using IPv4 0.0.0.0 (all network interfaces)," +
                                                  "otherwise bind to 127.0.0.1 (localhost).  This maybe necessary in systems that only run Flask")
    args = parser.parse_args()

    if args.all_addresses:
        bind_host = '0.0.0.0'
    else:
        bind_host = '127.0.0.1'

    if args.daemon:
        pid = None
        try:
            pid = os.fork()
        except OSError as e:
            raise Exception("%s [%d]" % (e.strerror, e.errno))

        if (pid == 0):
            os.setsid()
            app.run(threaded=True, host=bind_host)
        else:
            os._exit(0)
    else:
        app.run(threaded=True, host=bind_host)
