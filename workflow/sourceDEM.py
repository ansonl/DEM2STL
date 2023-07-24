import os

from constants import *

# Prepare source DEM
# Merge/Patch/Mosaic elevation models from different sources (no resampling using gdal_merge/r.patch) buildvrt,load in QGIS, export to workaround gdal_merge bug for large files, gdal_translate
# Match elevation model resolutions before merge if needed (nearest neighbor)
# Return full resolution and 250x250x resolution DEM filenames
def generateSourceDEMCommands(modelResolution):

    print("Prepare source DEM files")
    print()

    #merge SRTM
    SRTM_source_HGT_dir = 'srcdir/SRTM/'
    SRTM_merge_VRT_filename = 'north_america_srtm_wgs84.vrt'
    SRTM_merge_TIF_filename = 'north_america_srtm_wgs84.tif'
    SRTM_merge_buildVRT_cmd = f'gdalbuildvrt -resolution highest -overwrite {SRTM_merge_VRT_filename} {SRTM_source_HGT_dir}*.hgt'
    SRTM_merge_translate_cmd = f'gdal_translate -ot Int16 {GTIFF_creation_options_str} {SRTM_merge_VRT_filename} {SRTM_merge_TIF_filename}'

    print(f'# Merge SRTM tiles in {SRTM_source_HGT_dir} → {SRTM_merge_TIF_filename}')
    print(SRTM_merge_translate_cmd)
    print()

    #merge GMTED
    GMTED_source_TIF_dir = 'srcdir/GMTED2010/7-5-arc-second/mea/'
    GMTED_merge_VRT_filename = 'north_america_gmted2010_wgs84.vrt'
    GMTED_merge_TIF_filename = 'north_america_gmted2010_wgs84.tif'
    GMTED_merge_buildVRT_cmd = f'gdalbuildvrt -resolution highest -overwrite {GMTED_merge_VRT_filename} {GMTED_source_TIF_dir}*.tif'
    GMTED_merge_translate_cmd = f'gdal_translate -ot Int16 {GTIFF_creation_options_str} {GMTED_merge_VRT_filename} {GMTED_merge_TIF_filename}'

    print(f'# Merge GMTED tiles in {GMTED_source_TIF_dir} → {GMTED_merge_TIF_filename}')
    print(GMTED_merge_translate_cmd)
    print()

    #merge GMTED and SRTM buildvrt
    SRTM_GMTED_merge_VRT_filename = 'north_america_gmted2010_srtm_merge_wgs84.vrt'
    SRTM_GMTED_merge_TIF_filename = 'north_america_gmted2010_srtm_merge_wgs84.tif'
    SRTM_GMTED_merge_buildVRT_cmd = f'gdalbuildvrt -resolution highest -overwrite {SRTM_GMTED_merge_VRT_filename} {GMTED_merge_TIF_filename} {SRTM_merge_TIF_filename}'
    SRTM_GMTED_merge_translate_cmd = f'gdal_translate -ot Int16 {GTIFF_creation_options_str} {SRTM_GMTED_merge_VRT_filename} {SRTM_GMTED_merge_TIF_filename}'

    print(f'# Merge SRTM and GMTED tiles → {SRTM_GMTED_merge_TIF_filename}')
    print(SRTM_GMTED_merge_translate_cmd)
    print()

    #merge GMTED and SRTM buildvrt and warp to 102004 and downscale to 102004 
    #SRTM_GMTED_merge_resampling_method = 'average'
    #SRTM_GMTED_merge_102004_TIF_filename = 'north_america_gmted2010_srtm_merge_102004.tif'
    #SRTM_GMTED_merge_warp_102004_cmd = f'gdalwarp -overwrite -t_srs ESRI:102004 -r {SRTM_GMTED_merge_resampling_method}  -multi {GTIFF_creation_options_str} {GTIFF_write_options_str} {SRTM_GMTED_merge_VRT_filename} {SRTM_GMTED_merge_102004_TIF_filename}'

    #use merged GMTED and SRTM TIF in WGS84 and warp to 102004 and downscale to 500x500m with bilinear/average resampling (doing it in QGIS>export>save as does not seem to have gaps if reproject and downscale at same time)
    SRTM_GMTED_merge_102004_500m_target_srs = 'ESRI:102004'
    SRTM_GMTED_merge_102004_500m_target_resolution = modelResolution*2
    SRTM_GMTED_merge_102004_500m_resampling_method = 'average'
    SRTM_GMTED_merge_102004_500m_TIF_filename = f'north_america_gmted2010_srtm_merge_{get_trailing_number(SRTM_GMTED_merge_102004_500m_target_srs)}_{SRTM_GMTED_merge_102004_500m_target_resolution}m_{SRTM_GMTED_merge_102004_500m_resampling_method}.tif'
    SRTM_GMTED_merge_warp_102004_500m_cmd = f'gdalwarp -overwrite -t_srs {SRTM_GMTED_merge_102004_500m_target_srs} -tr {SRTM_GMTED_merge_102004_500m_target_resolution} {SRTM_GMTED_merge_102004_500m_target_resolution} -r {SRTM_GMTED_merge_102004_500m_resampling_method} -multi -of GTiff {GTIFF_creation_options_str} {GTIFF_write_options_str} {SRTM_GMTED_merge_TIF_filename} {SRTM_GMTED_merge_102004_500m_TIF_filename}'

    print(f'# Warp merged SRTM and GMTED DEM from WGS84 to {SRTM_GMTED_merge_102004_500m_target_srs} and downscale to {SRTM_GMTED_merge_102004_500m_target_resolution}x{SRTM_GMTED_merge_102004_500m_target_resolution}m resolution with {SRTM_GMTED_merge_102004_500m_resampling_method} resampling method → {SRTM_GMTED_merge_102004_500m_TIF_filename}')
    print('# Run this in one operation in QGIS>export>save as output dem does not seem to have gaps if reproject and downscale at same time in QGIS!')
    print('# ' + SRTM_GMTED_merge_warp_102004_500m_cmd)
    print()

    #250x250 upscale in bilinear
    SRTM_GMTED_merge_102004_500m_250m_target_srs = SRTM_GMTED_merge_102004_500m_target_srs
    SRTM_GMTED_merge_102004_500m_250m_target_resolution = modelResolution
    SRTM_GMTED_merge_102004_500m_250m_resampling_method = 'bilinear' #cubicspline
    SRTM_GMTED_merge_102004_500m_250m_TIF_filename = f'{os.path.splitext(SRTM_GMTED_merge_102004_500m_TIF_filename)[0]}_{SRTM_GMTED_merge_102004_500m_250m_target_resolution}m_{SRTM_GMTED_merge_102004_500m_250m_resampling_method}.tif'
    SRTM_GMTED_merge_102004_500m_250m_cmd = f'gdalwarp -overwrite -tr {SRTM_GMTED_merge_102004_500m_250m_target_resolution} {SRTM_GMTED_merge_102004_500m_250m_target_resolution} -r {SRTM_GMTED_merge_102004_500m_250m_resampling_method} -multi -of GTiff {GTIFF_creation_options_str} {GTIFF_write_options_str} {SRTM_GMTED_merge_102004_500m_TIF_filename} {SRTM_GMTED_merge_102004_500m_250m_TIF_filename}'

    print(f'# Upscale the merged SRTM and GMTED {SRTM_GMTED_merge_102004_500m_target_resolution}x{SRTM_GMTED_merge_102004_500m_target_resolution}m DEM to {SRTM_GMTED_merge_102004_500m_250m_target_resolution}x{SRTM_GMTED_merge_102004_500m_250m_target_resolution}m resolution with {SRTM_GMTED_merge_102004_500m_250m_resampling_method} resampling method → {SRTM_GMTED_merge_102004_500m_250m_TIF_filename}')
    print(SRTM_GMTED_merge_102004_500m_250m_cmd)
    print()

    return SRTM_GMTED_merge_TIF_filename, SRTM_GMTED_merge_102004_500m_250m_TIF_filename