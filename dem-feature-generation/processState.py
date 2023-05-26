import os
import math
from textwrap import dedent
import geopandas as gpd

# run from /dem-feature-generation/ directory

rasterResolution = 250
clipCRS = 'ESRI:102004'

boundaryPath = f'../sources/USCB/tl_2022_us_state/split_individual/'
sourceDEMRasterPath = f'../sources/north_america_gmted2010_srtm_merge_102004_500m_avg_250m_cubicspline.tif'
sourceMaskRasterPath = f'../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif'

clippedDEMRasterPath = f'../dem-feature-generation/source-dem-{rasterResolution}m-clipped/'
clippedMaskRasterPath = f'../dem-feature-generation/hydrographic-mask-{rasterResolution}m-clipped/'

outputCommandFile = './clip-raster-to-boundaries.sh'

allFiles = os.listdir(boundaryPath)
allFiles.sort(key=lambda f: os.stat(boundaryPath + f).st_size, reverse=False)

with open(outputCommandFile, 'w+') as cmdfp:
    entriesProcessed = 0
    for entry in allFiles:
        if entry.endswith('.gpkg'):
            input_file = boundaryPath + entry
            data = gpd.read_file(input_file)
            # data.head().bounds
            convertedData = data.to_crs(clipCRS)
            # convertedData.head().bounds

            # get state extent
            # print(f'{entry} {convertedData.total_bounds}')

            # extend state extents by 5000m in each direction which is 10 (500x500) pixels
            extendedExtents = [math.floor(convertedData.total_bounds[0]-5000), math.floor(convertedData.total_bounds[1]-5000),
                               math.ceil(convertedData.total_bounds[2]+5000), math.ceil(convertedData.total_bounds[3]+5000)]
            # ME [1925836.2845578345, 715547.1196991404, 2268720.5956089958, 1251148.1439610166]

            print(f'{entry} {extendedExtents}')

            entryName = entry.replace('.gpkg', '')
            entryClippedFileName = entryName + '.tif'

            clipDEMRasterCmd = ' '.join((
                'gdalwarp',
                f'-te {extendedExtents[0]} {extendedExtents[1]} {extendedExtents[2]} {extendedExtents[3]}',
                f'-te_srs {clipCRS}',
                '-wo "NUM_THREADS=ALL_CPUS"',
                '-r cubicspline',
                '-multi',
                '-of GTiff',
                '-co "COMPRESS=ZSTD"',
                '-co "PREDICTOR=2"',
                '-co "NUM_THREADS=ALL_CPUS"',
                '-overwrite',
                f'{sourceDEMRasterPath}',
                f'{clippedDEMRasterPath + entryClippedFileName}'))

            clipMaskRasterCmd = ' '.join((
                'gdalwarp',
                f'-te {extendedExtents[0]} {extendedExtents[1]} {extendedExtents[2]} {extendedExtents[3]}',
                f'-te_srs {clipCRS}',
                '-wo "NUM_THREADS=ALL_CPUS"',
                '-r cubicspline',
                '-multi',
                '-of GTiff',
                '-co "COMPRESS=ZSTD"',
                '-co "PREDICTOR=2"',
                '-co "NUM_THREADS=ALL_CPUS"',
                '-overwrite',
                f'{sourceMaskRasterPath}',
                f'{clippedMaskRasterPath + entryClippedFileName}'))

            cmdfp.write(f'echo Clipping rasters for {entry}' + '\n' +
                        f'time {clipDEMRasterCmd}' + '\n' +
                        f'time {clipMaskRasterCmd}' + '\n')
            entriesProcessed += 1
print(f'Write commands for {entriesProcessed} entries to {outputCommandFile}')

# gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 20.0 20.0 -te 1925836.2845578345 715547.1196991404 2268720.5956089958 1251148.1439610166 -te_srs ESRI:102004 ./dems/7-5-arc-second-merged-reproject-102004.tif ./dems/tmp/gmted-ME.tif -r cubicspline -multi -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"
