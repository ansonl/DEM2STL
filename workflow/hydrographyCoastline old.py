import os

from constants import *

def generateCoastlineDEMCommands(sourceDEMFilename):

    lakeClippedMasksPath = 'coastline/'
    lakeMaskFilename = 'coastline_hydrographic_mask_merge.vrt'
    lakeMaskInt16Filename = os.path.splitext(lakeMaskFilename)[0] + "_int16" + ".vrt"

    #load lakes data from lake-locations.json
    lakes = []

    for location in lakes:

        featureName = location['feature']
        clippedDEMFilename = featureName.replace(' ', '-') + '.tif'

        featureArea = location['area']
        #re
        extents = []
        extentsCRS = ''

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