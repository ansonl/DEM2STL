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

<PixelFunctionArguments op="raiseLandAIfNotInHydroMaskBAndScaleAt4m" />
<PixelFunctionArguments op="raiseLandAScaleAt4m" />
<PixelFunctionArguments op="deleteLandAIfInHydroMaskB" />
<PixelFunctionArguments op="keepLandAIfNotInHydroMaskB" />
"""

# minuend - subtrahend = difference
  
def globalLogScaleLandA(a):
  if a > 0:
    return math.sqrt(a) * 35#(math.log(a+1)/math.log(2)) *200
  elif a == 0:
    return 0
  elif a > -32768:
    return a #(math.log(abs(a)+1)/math.log(2)) *200
  else:
    return a

def runOperation(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize, raster_ysize, radius, gt, **kwargs):
  op = kwargs['op'].decode('utf-8')
  #import ctypes  # An included library with Python install.   
  #ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)

  print(f'Requested {op}')
  if op == 'globalLogScaleLandA':
    vGlobalLogScaleLandA = np.vectorize(globalLogScaleLandA)
    np.round_(vGlobalLogScaleLandA(in_ar[0]), decimals=4, out=out_ar)
  else:
    raise Exception(f'Invalid op {op}')

  #print(f'Completed {op}')