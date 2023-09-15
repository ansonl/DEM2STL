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

# Input elevation DEM-A and hydro mask-B. Output minuend DEM intermediate.
# Was intermediate step for raiseLandAScaleAt4m. No longer needed because r.lake flood will include below sea level locations touching the ocean.
"""
def raiseOverSeaLevelLandAIfInHydroMaskB(a, b):
  if a > 0:
    return a
  elif b > 0:
    return b
  else:
    return a
"""

# Input elevation DEM-A and hydro mask-B. Output subtrahend DEM.
def raiseLandAIfNotInHydroMaskBAndScaleAt4m(a, b):
  if a > 40: # 40m -> 80m
    return a + 40
  elif a > 0:
    return np.log(a+1)*80/np.log(41)
  else:
    return a

# Input elevation DEM-A and hydro mask-B. Output minuend DEM.
def raiseLandAScaleAt4m(a, b):
  if b > 0: #set 0 if covered by mask first to keep 0 to >0 land slope lower at coast
    return 0
  if a > 40: # 40m -> 79m
    return -50#a + 39
  elif a > 0:
    return -50#np.log(a+1)*79/np.log(41)
  else:
    return a
  
# Input elevation DEM-A and hydro mask-B. Output subtrahend DEM for translucent rivers thru the base. 
def deleteLandAIfInHydroMaskB(a, b):
  if a <= 0 and b > 0:
    return -50
  else:
    return a
  
# Input elevation DEM-A and hydro mask-B. Output single material print DEM.
def keepLandAIfNotInHydroMaskB(a, b):
  return 0
  
# Global log scale. Add 50 (popover height) before log scale.Transparent version. Output subtrahend DEM. raiseLandAIfNotInHydroMaskBAndScaleAt4m and deleteLandAIfInHydroMaskB adapted for log scale
# ((B > 0 ) * -32768) + ((B <= 0 ) * ((A > 0 ) * ln("A"+50))) + ((B <= 0 ) * ((A < 0 ) * (A > -32768 ) * ln(abs("A"))))
def globalLogScaleLandADeleteIfInHydroMaskB(a,b):
  if b > 0:
    return -32768
  elif a > 0 :
    return math.sqrt(a) * 35 + 65 #(math.log(a+1)/math.log(2)) *200
  elif a == 0:
    return 0
  elif a > -32768:
    return -1 * math.sqrt(abs(a)) * 35 #(math.log(abs(a)+1)/math.log(2)) *200
  else:
    return a

# Global log scale. Output minuend DEM. raiseLandAScaleAt4m adapted for log scale
# ((A > 0 ) * ln("A")) + ((A < 0 ) * (A > -32768 ) * ln(abs("A")))
def globalLogScaleLandA(a):
  if a > 0:
    return math.sqrt(a) * 35 + 65#(math.log(a+1)/math.log(2)) *200
  elif a == 0:
    return 0
  elif a > -32768:
    return -1 * math.sqrt(abs(a)) * 35 #(math.log(abs(a)+1)/math.log(2)) *200
  else:
    return a

def runOperation(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize, raster_ysize, radius, gt, **kwargs):
  op = kwargs['op'].decode('utf-8')
  #import ctypes  # An included library with Python install.   
  #ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)

  print(f'Requested {op}')
  if op == 'raiseLandAIfNotInHydroMaskBAndScaleAt4m':
    vRaiseLandAIfNotInHydroMaskBAndScaleAt4m = np.vectorize(raiseLandAIfNotInHydroMaskBAndScaleAt4m)
    np.round_(vRaiseLandAIfNotInHydroMaskBAndScaleAt4m(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'raiseLandAScaleAt4m':
    vraiseLandAScaleAt4m = np.vectorize(raiseLandAScaleAt4m)
    np.round_(vraiseLandAScaleAt4m(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'deleteLandAIfInHydroMaskB':
    vDeleteLandAIfInHydroMaskB = np.vectorize(deleteLandAIfInHydroMaskB)
    np.round_(vDeleteLandAIfInHydroMaskB(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'keepLandAIfNotInHydroMaskB':
    vKeepLandAIfNotInHydroMaskB = np.vectorize(keepLandAIfNotInHydroMaskB)
    np.round_(vKeepLandAIfNotInHydroMaskB(in_ar[0], in_ar[1]), out=out_ar)
  elif op == 'globalLogScaleLandADeleteIfInHydroMaskB':
    vGlobalLogScaleLandADeleteIfInHydroMaskB = np.vectorize(globalLogScaleLandADeleteIfInHydroMaskB)
    np.round_(vGlobalLogScaleLandADeleteIfInHydroMaskB(in_ar[0], in_ar[1]), decimals=4, out=out_ar)
  elif op == 'globalLogScaleLandA':
    vGlobalLogScaleLandA = np.vectorize(globalLogScaleLandA)
    np.round_(vGlobalLogScaleLandA(in_ar[0]), decimals=4, out=out_ar)
  else:
    raise Exception(f'Invalid op {op}')

  #print(f'Completed {op}')