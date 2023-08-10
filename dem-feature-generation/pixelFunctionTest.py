import numpy as np

import math

def globalLogScaleLandA(a):
  if a > 0:
    return a+0.1 #math.log(float(a))
  elif a == 0:
    return 0
  elif a > -32768:
    return -1 * math.log(float(abs(a)))
  else:
    return a
  
def runOperation(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize, raster_ysize, radius, gt, **kwargs):
  op = kwargs['op'].decode('utf-8')
  vGlobalLogScaleLandA = np.vectorize(globalLogScaleLandA)
  np.round_(vGlobalLogScaleLandA(in_ar[0]), decimals=4, out=out_ar)
