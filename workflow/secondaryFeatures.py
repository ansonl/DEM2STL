from constants import *

def test():
    print("testing")

def generateSecondaryFeatureCommands():
    return
    

def generateRegionBoundaryMaskCommands():
    print('# Buffer region boundary polygons to 1000m')
    print('# Rasterize buffered boundaries. This should also merge the adjacent polygon edges.')
    print('# Reproject to 102004 (near)')
    print('# Downscale to 250mx250m (max)')
    print('# VRT DEM Raster Calc step later: Set to 0 where same cells are not set to 0 in hydrographic mask')
    return

def generatePixelFunctionPatchScript(VRTFilename, pixelFunctionArgumentOp):
    return f'python3 -c "exec(\"import secondaryFeatures\nsecondaryFeatures.patchVRTPixelFunction(\"{VRTFilename}\",\"{pixelFunctionArgumentOp}\")\")"'

def patchVRTPixelFunction(VRTFilename, pixelFunctionArgumentOp):
    vrt_tree = etree.parse(VRTFilename)
    vrt_root = vrt_tree.getroot()
    vrtband1 = vrt_root.findall(".//VRTRasterBand[@band='1']")[0]

    vrtband1.set("subClass","VRTDerivedRasterBand")
    vrtband1.set("dataType","Float32")
    pixelFunctionType = etree.SubElement(vrtband1, 'PixelFunctionType')
    pixelFunctionType.text = "rasterPixelFunctions.runOperation"
    pixelFunctionLanguage = etree.SubElement(vrtband1, 'PixelFunctionLanguage')
    pixelFunctionLanguage.text = "Python"
    pixelFunctionArguments = etree.SubElement(vrtband1, 'PixelFunctionArguments')
    pixelFunctionArguments.set("op", pixelFunctionArgumentOp)
    
    vrt_tree.write(VRTFilename, pretty_print=True)

def generateDEMRasterCalculationCommands(outputResolution, sourceDEMOutputPrintedResFilename,hydrographicMaskRasterFilename):
    raiseLandAIfNotInHydroMaskBAndScaleAt4m_name = 'raiseLandAIfNotInHydroMaskBAndScaleAt4m'
    raiseLandAIfNotInHydroMaskBAndScaleAt4m_VRT_filename = f'{raiseLandAIfNotInHydroMaskBAndScaleAt4m_name}.vrt'
    raiseLandAIfNotInHydroMaskBAndScaleAt4m_TIF_filename = f'{raiseLandAIfNotInHydroMaskBAndScaleAt4m_name}-{outputResolution}m-raised-460m.tif'
    raiseLandAIfNotInHydroMaskBAndScaleAt4m_buildVRT_cmd = f'gdalbuildvrt -resolution highest -overwrite {raiseLandAIfNotInHydroMaskBAndScaleAt4m_VRT_filename} {sourceDEMOutputPrintedResFilename} {hydrographicMaskRasterFilename}'
    raiseLandAIfNotInHydroMaskBAndScaleAt4m_translate_cmd = f'gdal_translate -ot Int16 {GTIFF_creation_options_str} {raiseLandAIfNotInHydroMaskBAndScaleAt4m_VRT_filename} {raiseLandAIfNotInHydroMaskBAndScaleAt4m_TIF_filename} {configuration_keywords_str}'

    print(f'# Build VRT for {raiseLandAIfNotInHydroMaskBAndScaleAt4m_name} using {sourceDEMOutputPrintedResFilename} + {hydrographicMaskRasterFilename} → {raiseLandAIfNotInHydroMaskBAndScaleAt4m_VRT_filename}')
    print(raiseLandAIfNotInHydroMaskBAndScaleAt4m_buildVRT_cmd)
    print(f'# Patch VRT for {raiseLandAIfNotInHydroMaskBAndScaleAt4m_name} {raiseLandAIfNotInHydroMaskBAndScaleAt4m_VRT_filename}')
    print(generatePixelFunctionPatchScript(raiseLandAIfNotInHydroMaskBAndScaleAt4m_VRT_filename, raiseLandAIfNotInHydroMaskBAndScaleAt4m_name))



    #run translate
    print()

    raiseLandAScaleAt4m_name = 'raiseLandAScaleAt4m'
    raiseLandAScaleAt4m_VRT_filename = f'{raiseLandAScaleAt4m_name}.vrt'
    raiseLandAScaleAt4m_TIF_filename = f'{raiseLandAScaleAt4m_name}-{outputResolution}m-raised-400m.tif'
    raiseLandAScaleAt4m_buildVRT_cmd = f'gdalbuildvrt -resolution highest -overwrite {raiseLandAScaleAt4m_VRT_filename} {sourceDEMOutputPrintedResFilename} {hydrographicMaskRasterFilename}'
    raiseLandAScaleAt4m_translate_cmd = f'gdal_translate -ot Int16 {GTIFF_creation_options_str} {raiseLandAScaleAt4m_VRT_filename} {raiseLandAScaleAt4m_TIF_filename} {configuration_keywords_str}'

    print(f'# Build VRT for {raiseLandAScaleAt4m_name} using {sourceDEMOutputPrintedResFilename} + {hydrographicMaskRasterFilename} → {raiseLandAScaleAt4m_VRT_filename} → {raiseLandAScaleAt4m_TIF_filename}')
    print()

    deleteLandAIfInHydroMaskB_name = 'deleteLandAIfInHydroMaskB'
    deleteLandAIfInHydroMaskB_VRT_filename = f'{deleteLandAIfInHydroMaskB_name}.vrt'
    deleteLandAIfInHydroMaskB_TIF_filename = f'{deleteLandAIfInHydroMaskB_name}-{outputResolution}m-raised-460m.tif'
    deleteLandAIfInHydroMask_buildVRT_cmd = f'gdalbuildvrt -resolution highest -overwrite {deleteLandAIfInHydroMaskB_VRT_filename} {raiseLandAIfNotInHydroMaskBAndScaleAt4m_TIF_filename} {hydrographicMaskRasterFilename}'
    deleteLandAIfInHydroMask_translate_cmd = f'gdal_translate -ot Int16 {GTIFF_creation_options_str} {deleteLandAIfInHydroMaskB_VRT_filename} {deleteLandAIfInHydroMaskB_TIF_filename} {configuration_keywords_str}'

    print(f'# Build VRT for {deleteLandAIfInHydroMaskB_name} (thru cut) using {raiseLandAIfNotInHydroMaskBAndScaleAt4m_TIF_filename} + {hydrographicMaskRasterFilename} → {deleteLandAIfInHydroMaskB_VRT_filename} → {deleteLandAIfInHydroMaskB_TIF_filename}')
    print()


    keepLandAIfNotInHydroMaskB_name = 'keepLandAIfNotInHydroMaskB'
    keepLandAIfNotInHydroMaskB_VRT_filename = f'{keepLandAIfNotInHydroMaskB_name}.vrt'
    keepLandAIfNotInHydroMaskB_TIF_filename = f'{keepLandAIfNotInHydroMaskB_name}-{outputResolution}m.tif'
    keepLandAIfNotInHydroMaskB_buildVRT_cmd = f'gdalbuildvrt -resolution highest -overwrite {keepLandAIfNotInHydroMaskB_VRT_filename} {sourceDEMOutputPrintedResFilename} {hydrographicMaskRasterFilename}'
    keepLandAIfNotInHydroMaskB_translate_cmd = f'gdal_translate -ot Int16 {GTIFF_creation_options_str} {keepLandAIfNotInHydroMaskB_VRT_filename} {keepLandAIfNotInHydroMaskB_TIF_filename} {configuration_keywords_str}'
    print(f'# Build VRT for {keepLandAIfNotInHydroMaskB_name} (single print with rivers debossed) using {sourceDEMOutputPrintedResFilename} + {hydrographicMaskRasterFilename} → {keepLandAIfNotInHydroMaskB_VRT_filename} → {keepLandAIfNotInHydroMaskB_TIF_filename}')
    print()

from lxml import etree

