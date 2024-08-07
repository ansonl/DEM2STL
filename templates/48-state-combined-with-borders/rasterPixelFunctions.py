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

linearScale = 40
borderAddElevationHeight = 1000 * linearScale


def scaleBase(a, extraHeight):
  if a > 0:
    return a * linearScale + extraHeight
  elif a== 0:
    return a * linearScale + extraHeight/2
  else:
    return a

# border model
def borderModel(a, b):
  if b > 0:
    return scaleBase(a, borderAddElevationHeight) + b*100
  else:
    return -32768

# Input elevation DEM-A. Output A*5.
def baseModel(a, b):
  if b > 0:
    return scaleBase(a, 0)
  else:
    return scaleBase(a, borderAddElevationHeight)

def scaleSqrtBase(a, extraHeight):
  if a > 0:
    return math.log(a+100) * 27000 + extraHeight
  elif a == 0:
    return math.log(a+100) * 27000 + extraHeight/2
  else:
    return a

# border model sqrt
def sqrtScaleBorderModel(a,b):
  if b > 0:
    return scaleSqrtBase(a, borderAddElevationHeight) + b * 100
  else:
    return -32768

# Global log base 2 scale. 
def sqrtScaleBaseModel(a, b):
  if b > 0:
    return scaleSqrtBase(a, 0) * 0.9
  else:
    return scaleSqrtBase(a, borderAddElevationHeight)

def runOperation(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize, raster_ysize, radius, gt, **kwargs):
  op = kwargs['op'].decode('utf-8')
  #import ctypes  # An included library with Python install.   
  #ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)

  print(f'Requested {op}')
  if op == 'borderModel':
    vRaiseLandAIfNotInHydroMaskBAndScale = np.vectorize(borderModel)
    np.round_(vRaiseLandAIfNotInHydroMaskBAndScale(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'baseModel':
    vraiseLandAAndScale = np.vectorize(baseModel)
    np.round_(vraiseLandAAndScale(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'sqrtScaleBorderModel':
    vRaiseLandAIfNotInHydroMaskBAndScale = np.vectorize(sqrtScaleBorderModel)
    np.round_(vRaiseLandAIfNotInHydroMaskBAndScale(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'sqrtScaleBaseModel':
    vGlobalScaleLandA = np.vectorize(sqrtScaleBaseModel)
    np.round_(vGlobalScaleLandA(in_ar[0], in_ar[1]), decimals=4, out=out_ar)
  else:
    raise Exception(f'Invalid op {op}')

  #print(f'Completed {op}')