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

# Input elevation DEM-A and hydro mask-B. Output subtrahend DEM.
def raiseLandAIfNotInHydroMaskBAndScaleOrig(a, b):
  if b > 0:
    if a > 0:
      return a
    else: # if A is <= 0m and is covered by mask, set to NODATA so that it is not 3D generated. This will allow oceans to be show from other model. 
      return -32768 
  elif a > 40: # 40m -> 450m
    return a + 410
  elif a > 0:
    return np.log(a+1)*450/np.log(41)
  else:
    return a
  
def raiseLandAIfNotInHydroMaskBAndScale(a, b):
  if b > 0:
    if a > 0:
      return a
    else: # if A is <= 0m and is covered by mask, set to NODATA so that it is not 3D generated. This will allow oceans to be show from other model. 
      return -32768 
  elif a > 40: # 40m -> 400m
    return a + 360
  elif a > 0:
    return np.log(a+1)*400/np.log(41)
  else:
    return a

# Input elevation DEM-A. Output minuend DEM.
def raiseLandAAndScale(a):
  if a > 40: # 40m -> 400m
    return a + 360
  elif a > 0:
    return np.log(a+1)*400/np.log(41)
  else:
    return a
  
# Input elevation DEM-A and hydro mask-B. Output subtrahend DEM for translucent rivers thru the base. 
def deleteLandAIfInHydroMaskB(a, b):
  if b > 0:
    return -32768
  else:
    return a
  
# Input elevation DEM-A and hydro mask-B. Output single material print DEM.
#input land A, hydro mask B, coastline only mask C
def keepLandAIfNotInHydroMaskB(a, b, c):
  if b > 0:
    if a > 0:
      return a
    elif c > 0: # if A is <= 0m and is covered by combined hydro mask AND coastline mask, set to NODATA so that it is not 3D generated. This allows us to start the base thickness from below sea level.
      return -32768 
    else: #otherwise, A is sea level or below sea level but considered inland and should be kept at it's below sea level elevation to be printed
      return a 
  elif a > 0:
      return a + 100
  return a

def runOperation(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize, raster_ysize, radius, gt, **kwargs):
  op = kwargs['op'].decode('utf-8')
  #import ctypes  # An included library with Python install.   
  #ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)

  print(f'Requested {op}')
  if op == 'raiseLandAIfNotInHydroMaskBAndScale':
    vRaiseLandAIfNotInHydroMaskBAndScale = np.vectorize(raiseLandAIfNotInHydroMaskBAndScale)
    np.round_(vRaiseLandAIfNotInHydroMaskBAndScale(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'raiseLandAAndScale':
    vraiseLandAAndScale = np.vectorize(raiseLandAAndScale)
    np.round_(vraiseLandAAndScale(in_ar[0]), out=out_ar)
  elif op == 'deleteLandAIfInHydroMaskB':
    vDeleteLandAIfInHydroMaskB = np.vectorize(deleteLandAIfInHydroMaskB)
    np.round_(vDeleteLandAIfInHydroMaskB(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'keepLandAIfNotInHydroMaskB':
    vKeepLandAIfNotInHydroMaskB = np.vectorize(keepLandAIfNotInHydroMaskB)
    np.round_(vKeepLandAIfNotInHydroMaskB(in_ar[0], in_ar[1], in_ar[2]), out=out_ar)
  else:
    raise Exception(f'Invalid op {op}')

  #print(f'Completed {op}')