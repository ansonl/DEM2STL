from osgeo import gdal
from osgeo import gdalconst
from osgeo.gdalconst import GA_ReadOnly

import sys

# Get TIF extents to 3d print
data = gdal.Open(sys.argv[1], GA_ReadOnly)
geoTransform = data.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * data.RasterXSize
miny = maxy + geoTransform[5] * data.RasterYSize
print([minx, miny, maxx, maxy])
print([f"bllat {miny}", f"bllon {minx}", f"trlat {maxy}", f"trlon {maxx}"])