import numpy as np

import math

#Powershell envvar settings
"""
$env:GDAL_VRT_ENABLE_PYTHON = 'YES'
$env:PYTHONPATH = './'
"""

#Add subClass="VRTDerivedRasterBand" to <VRTRasterBand>
"""
Change dataType="Float32" in <VRTRasterBand> if in Int16 due to numpy.round only outputting float array
<VRTRasterBand dataType="Float32" band="1" subClass="VRTDerivedRasterBand">
"""
#Add PixelFunction to VRT inside <VRTRasterBand>
"""
<PixelFunctionLanguage>Python</PixelFunctionLanguage>
<PixelFunctionType>demFeatureProcessing.runOperation</PixelFunctionType>
<PixelFunctionArguments op="OPERATION" />

e.g. one of the below

<PixelFunctionArguments op="raiseLandAIfNotInHydroMaskBAndScale" />
<PixelFunctionArguments op="raiseLandAAndScale" />
<PixelFunctionArguments op="deleteLandAIfInHydroMaskB" />
<PixelFunctionArguments op="keepLandAIfNotInHydroMaskB" />
"""

# minuend - subtrahend = difference

# Input elevation DEM-A and mask B. Output A*5 + B
def raiseLandAByBAndScale(a, b):
  return a * 5 + b*2 - 1

# Input elevation DEM-A. Output A*5.
def raiseLandAAndScale(a):
  return a * 5

def runOperation(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize, raster_ysize, radius, gt, **kwargs):
  op = kwargs['op'].decode('utf-8')
  #import ctypes  # An included library with Python install.   
  #ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)

  print(f'Requested {op}')
  if op == 'raiseLandAByBAndScale':
    vRaiseLandAIfNotInHydroMaskBAndScale = np.vectorize(raiseLandAByBAndScale)
    np.round_(vRaiseLandAIfNotInHydroMaskBAndScale(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'raiseLandAAndScale':
    vraiseLandAAndScale = np.vectorize(raiseLandAAndScale)
    np.round_(vraiseLandAAndScale(in_ar[0]), out=out_ar)
  else:
    raise Exception(f'Invalid op {op}')

  #print(f'Completed {op}')