import os
import json

from constants import *

def generateCoastlineDEMCommands(sourceDEMFilename):

    lakeClippedMasksPath = 'coastline/'
    lakeMaskFilename = 'coastline_hydrographic_mask_merge.vrt'
    lakeMaskInt16Filename = os.path.splitext(lakeMaskFilename)[0] + "_int16" + ".vrt"

    #load lakes data from lake-locations.json
    input_file = open ('../hydrographic-masks/lake-locations.json')
    lakes = json.load(input_file)

    for location in lakes:

        featureName = location['feature']
        clippedDEMFilename = featureName.replace(' ', '-') + '.tif'

        featureExtent = location['extent']
        #re
        extentMatches = re.findall('([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+) \[([A-Z:0-9]*)\]', featureExtent)
        if len(extentMatches) == 5:
            extents = extentMatches[0:4]
            extentsCRS = extentMatches[4]
        else:
            print(f'# Could not parse feature extent for {featureName}. Got {len(extentMatches)}/5 matches.')
            continue

        featureStart = location['start']

        featureElevation = location['elevation']

        clipRasterCmd = ' '.join((
            'gdalwarp',
            f'-te {extents[0]} {extents[1]} {extents[2]} {extents[3]}',
            f'-te_srs {extentsCRS}',
            f'{GTIFF_write_options_str}',
            '-r cubicspline',
            '-multi',
            '-of GTiff',
            f'{GTIFF_creation_options_str}',
            '-overwrite',
            f'{sourceDEMFilename}',
            f'{clippedDEMFilename}'
        ))
        
        print(f'# Clip lake feature {featureName} - source DEM {sourceDEMFilename} → {clippedDEMFilename}')
        print(clipRasterCmd)
        print(f'# Run grass.lake with:\nStart: {featureStart}\nElevation: {featureElevation}\nLake raster location: {lakeClippedMasksPath}{clippedDEMFilename}')
        print()

    print(f'# Merge all lake rasters in {lakeClippedMasksPath}* → {lakeMaskFilename}')
    print(f'gdalbuildvrt -resolution highest -overwrite {lakeMaskFilename} {lakeClippedMasksPath}/*.tif')
    print()

    print(f'# Set merged lake VRT data type from Float32 to Int16 to save space - {lakeMaskFilename} → {lakeMaskInt16Filename}')
    print(f'gdal_translate -ot Int16 {lakeMaskFilename} {lakeMaskInt16Filename}')
    print()

    return lakeMaskInt16Filename

# all inputs must be WGS84 CRS
def generateHydrographicMaskFinalCommands(coastlinesFilename, streamsFilename, lakesFilename, targetSRS, modelResolution):

    hydrographicMask_merge_filename = "north_america_hydrographic_mask_merge.vrt"

    print(f'# Merge coastline, hydro1k, hydrolakes masks - {coastlinesFilename} {streamsFilename} {lakesFilename} → {hydrographicMask_merge_filename}')
    print(f'gdalbuildvrt -resolution highest -overwrite {hydrographicMask_merge_filename} {coastlinesFilename} {streamsFilename} {lakesFilename}')
    print()

    hydrographicMask_reproject_filename = os.path.splitext(hydrographicMask_merge_filename)[0] + "_102004" + ".vrt"
    hydrographicMask_reproject_resampling_method = "near"

    hydrographicMask_reproject_cmd = ' '.join((
        'gdalwarp',
        f'-t_srs {targetSRS}', #ESRI:102004
        f'-r {hydrographicMask_reproject_resampling_method}',
        '-multi',
        '-overwrite',
        f'{hydrographicMask_merge_filename}',
        f'{hydrographicMask_reproject_filename}'
    ))

    print(f'# Reproject hydrographic mask merge to {targetSRS} CRS - {hydrographicMask_merge_filename} → {hydrographicMask_reproject_filename}')
    print(hydrographicMask_reproject_cmd)
    print()

    hydrographicMask_reproject_250m_VRT_filename = os.path.splitext(hydrographicMask_reproject_filename)[0] + "_250m" + ".vrt"
    hydrographicMask_reproject_250m_TIF_filename = os.path.splitext(hydrographicMask_reproject_250m_VRT_filename)[0] + ".tif"
    hydrographicMask_reproject_250m_target_resolution = 250
    hydrographicMask_reproject_250m_resampling_method = "max"

    hydrographicMask_reproject_250m_buildVRT_cmd = ' '.join((
        'gdalwarp',
        f'-tr {hydrographicMask_reproject_250m_target_resolution} {hydrographicMask_reproject_250m_target_resolution}',
        f'-r {hydrographicMask_reproject_250m_resampling_method}',
        '-multi',
        '-overwrite',
        f'{hydrographicMask_reproject_filename}',
        f'{hydrographicMask_reproject_250m_VRT_filename}'
    ))

    hydrographicMask_reproject_250m_translate_cmd = ' '.join((
        'gdal_translate',
        f'-ot Int16',
        f'{GTIFF_creation_options_str}',
        f'{hydrographicMask_reproject_250m_VRT_filename}',
        f'{hydrographicMask_reproject_250m_TIF_filename}'
    ))

    print(f'# Downscale hydrographic mask reproject to {hydrographicMask_reproject_250m_target_resolution}x{hydrographicMask_reproject_250m_target_resolution}m resolution. Create VRT first for previewing. - {hydrographicMask_reproject_filename} → {hydrographicMask_reproject_250m_VRT_filename}')
    print(hydrographicMask_reproject_250m_buildVRT_cmd)
    print()

    print(f'# Create {hydrographicMask_reproject_250m_target_resolution}x{hydrographicMask_reproject_250m_target_resolution}m resolution TIF from VRT - {hydrographicMask_reproject_250m_VRT_filename} → {hydrographicMask_reproject_250m_TIF_filename}')
    print(hydrographicMask_reproject_250m_translate_cmd)
    print()

    return hydrographicMask_reproject_250m_TIF_filename