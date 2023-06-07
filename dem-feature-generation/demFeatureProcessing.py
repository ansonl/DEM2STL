import numpy as np

#Powershell envvar settings
#$env:GDAL_VRT_ENABLE_PYTHON = 'YES'
#$env:PYTHONPATH = './'

#Add subClass="VRTDerivedRasterBand" to <VRTRasterBand>
#Change dataType="Float32" in <VRTRasterBand> if in Int16 due to numpy.round only outputting float array
#<VRTRasterBand dataType="Float32" band="1" subClass="VRTDerivedRasterBand">
#Add PixelFunction to VRT inside <VRTRasterBand>
#<PixelFunctionLanguage>Python</PixelFunctionLanguage>
#<PixelFunctionType>demFeatureProcessing.runOperation</PixelFunctionType>
#one of the below
#<PixelFunctionArguments op="raiseOverSeaLevelLandAIfInHydroMaskB" />
#<PixelFunctionArguments op="raiseLandAIfNotInHydroMaskBAndScaleAt4m" />
#<PixelFunctionArguments op="raiseLandAScaleAt4m" />

# minuend - subtrahend = difference

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
    if a > 10:
      return a
    elif a > 0:
      return a
    else: # if A is <= 0m and is covered by mask, set to NODATA so that it is not 3D generated. This will allow oceans to be show from other model. 
      return -32768 
  elif a > 40: # 40m -> 450m
    return a + 410
  elif a > 0:
    return np.log(a+1)*450/np.log(41)
  else:
    return a

# Input minuend DEM-A and hydro mask-B. Output minuend DEM.
def raiseLandAScaleAt4m(a, b):
  if a > 40: # 40m -> 400m
    return a + 360
  elif a > 0:
    return np.log(a+1)*400/np.log(41)
  else:
    return a
  
# Input elevation DEM-A and hydro mask-B. Output single material print DEM.
def keepLandAIfNotInHydroMaskB(a, b):
  if b > 0:
    if a > 0:
      return a
    else: # if A is <= 0m and is covered by mask, set to NODATA so that it is not 3D generated. This allows us to start the base thickness from below sea level.
      return -32768 
  elif a > 0:
    return a + 100
  else:
    return a

def runOperation(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize, raster_ysize, radius, gt, **kwargs):
  op = kwargs['op'].decode('utf-8')
  #import ctypes  # An included library with Python install.   
  #ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)

  #print(f'Requested {op}')
  if op == 'raiseOverSeaLevelLandAIfInHydroMaskB':
    vRaiseOverSeaLevelLandAIfInHydroMaskB = np.vectorize(raiseOverSeaLevelLandAIfInHydroMaskB)
    np.round_(vRaiseOverSeaLevelLandAIfInHydroMaskB(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'raiseLandAIfNotInHydroMaskBAndScaleAt4m':
    vRaiseLandAIfNotInHydroMaskBAndScaleAt4m = np.vectorize(raiseLandAIfNotInHydroMaskBAndScaleAt4m)
    np.round_(vRaiseLandAIfNotInHydroMaskBAndScaleAt4m(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'raiseLandAScaleAt4m':
    vraiseLandAScaleAt4m = np.vectorize(raiseLandAScaleAt4m)
    np.round_(vraiseLandAScaleAt4m(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'keepLandAIfNotInHydroMaskB':
    vKeepLandAIfNotInHydroMaskB = np.vectorize(keepLandAIfNotInHydroMaskB)
    np.round_(vKeepLandAIfNotInHydroMaskB(in_ar[0], in_ar[1]), out=out_ar)
  else:
    raise Exception(f'Invalid op {op}')

  #print(f'Completed {op}')