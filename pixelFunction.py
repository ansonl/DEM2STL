#set GDAL_VRT_ENABLE_PYTHON=YES

import numpy as np


def add(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize, raster_ysize, buf_radius, gt, **kwargs):
  np.round_(np.clip(np.sum(in_ar, axis=0, dtype='uint16'), 0, 255), out=out_ar)

# Input hydro mask A, B, C. Output combined hydro mask
def addHydroMasksABC(a, b, c):
  return a + b + c

# final boolean subtraction: minuend - subtrahend = difference

# Input elevation DEM-A and hydro mask-B. Output minuend DEM intermediate.
def raiseOverSeaLevelLandAIfInHydroMaskB(a, b):
  if a > 0:
    return a
  elif b > 0:
    return b
  else:
    return a

# Input elevation DEM-A and hydro mask-B. Output subtrahend DEM.
def raiseLandAIfNotInHydroMaskBAndScaleAt4m(a, b):
  if b > 0:
    return a
  elif a > 4:
    return a + 460
  elif a > 0:
    return a + a * 115
  else:
    return a

# Input minuend DEM-A and hydro mask-B. Output minuend DEM.
def raiseLandAScaleAt4m(a, b):
  if a > 4:
    return a + 400
  elif a > 0:
    return a + a * ((b > 0) * 14 + 100)
  else:
    return a
  
vRaiseOverSeaLevelLandAIfInHydroMaskB = np.vectorize(raiseOverSeaLevelLandAIfInHydroMaskB)

def applyOp(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize, raster_ysize, buf_radius, gt, **kwargs):
  np.round_(vRaiseOverSeaLevelLandAIfInHydroMaskB(in_ar[0], in_ar[1]), out=out_ar)
