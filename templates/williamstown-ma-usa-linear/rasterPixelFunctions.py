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
<PixelFunctionArguments op="raiseLandAAndScale" />
<PixelFunctionArguments op="deleteLandAIfInHydroMaskB" />
<PixelFunctionArguments op="keepLandAIfNotInHydroMaskB" />
"""

# minuend - subtrahend = difference

# Global sqrt scale. Output minuend DEM. raiseLandAScaleAt4m adapted for log scale
# ((A > 0 ) * ln("A")) + ((A < 0 ) * (A > -32768 ) * ln(abs("A")))
#we want 4000m=4000m in real:scaled
def globalScaleLandA(a):
  if a > 0:
    return math.sqrt(a) * 57#we don't add a constant since we raise land later by 410 in the next step #final is about sqrt(x)*57+410
  #(math.log(a+1)/math.log(2)) *200
  elif a == 0:
    return 0
  elif a > -32768:
    return a #-1 * math.sqrt(abs(a)) * 35 #(math.log(abs(a)+1)/math.log(2)) *200
  else:
    return a

# Input elevation DEM-A and hydro mask-B. Output subtrahend DEM.
def raiseLandAIfNotInHydroMaskBAndScale(a, b):
  if b > 0:
    if b == 1:
      return a - 55
    elif b == 2:
      return a - 75
    elif b == 3:
      return 0
    else:
      print(f"got unmapped b mask value of {b}")
      return a + 10
  else:
    return a + 10

# Input elevation DEM-A and hydro mask-B. Output minuend DEM.
# clip dem by boundary buffer only polygon to find best border elev with raster statistics {'MAX': 1064.0,'MEAN': 541.5730188373842,'MIN': 169.0,
def raiseLandAAndScale(a, b):
  if b == 3:
    if a > 650:
      return a + 10
    else:
      return 650 + 10
  else:
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
    np.round_(vraiseLandAAndScale(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'globalScaleLandA':
    vGlobalScaleLandA = np.vectorize(globalScaleLandA)
    np.round_(vGlobalScaleLandA(in_ar[0]), decimals=4, out=out_ar)
  else:
    raise Exception(f'Invalid op {op}')

  #print(f'Completed {op}')