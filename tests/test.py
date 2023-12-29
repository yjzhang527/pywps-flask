from qgis._core import QgsVectorLayer

# processing.run("native:mergevectorlayers", {
#     'LAYERS': ['E:/projects/qgis/pywps-flask/static/requests/temp_ilx46x.json',
#                'E:/projects/qgis/pywps-flask/static/requests/temp_iwrE47.json'],
#     'CRS': 'EPSG:4326',
#     'OUTPUT': 'E:/projects/qgis/pywps-flask/static/TEMPORARY_OUTPUT1'})
#
# processing.run("native:mergevectorlayers", {
#     'LAYERS': [{
#         "data": "114.34378012999998,30.55570404089998,114.37498245209999,30.586936539999996",
#         "crss": ["EPSG:4326"],
#         "dimensions ": 2
#     },
#         {
#             "data": "114.34378012999998,30.55570404089998,114.37498245209999,30.586936539999996",
#             "crss": ["EPSG:4326"],
#             "dimensions ": 2
#         }],
#     'CRS': 'EPSG:4326',
#     'OUTPUT': 'E:/projects/qgis/pywps-flask/static/TEMPORARY_OUTPUT1'})
#
#
# bbox1 = "114.34378012999998,30.55570404089998,114.37498245209999,30.586936539999996"
# bbox2 = "115.0,31.0,116.0,32.0"
#
# result = processing.run("native:mergevectorlayers", {
#     'LAYERS': ["114.34378012999998,30.55570404089998,114.37498245209999,30.586936539999996", "115.0,31.0,116.0,32.0"],
#     'CRS': 'EPSG:4326',
#     'OUTPUT': 'E:/projects/qgis/pywps-flask/static/TEMPORARY_OUTPUT1'
# })
#
# QgsVectorLayer()

from osgeo import gdal, ogr

input_tiff = r'data/ASTGTM2_N05W058_dem/ASTGTM2_N05W058_dem.tif'
output_tiff = r'data/ASTGTM2_N05W058_dem/ASTGTM2_N05W058_dem_clip.tif'
geojson_file = r'data/clip.json'

options = gdal.WarpOptions(
    cutlineDSName=geojson_file,
    cropToCutline=True,
    cutlineWhere=None,
    dstNodata=0  # 背景值设置无色
)
gdal.Warp(output_tiff, input_tiff, options=options)