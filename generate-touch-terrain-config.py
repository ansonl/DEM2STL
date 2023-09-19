import os
# Set imports based on environment and packages
# import gdal
# from gdalconst import GA_ReadOnly
from osgeo import gdal
from osgeo import gdalconst
from osgeo.gdalconst import GA_ReadOnly

import json

import sys

import argparse

# File structure should be like below
#
# >geographic-data
#   >dems/1000m-clipped
#     -XX.tif
#   >state_stls <-generated state stl files
#     -example_config.json
#     -TouchTerrain_standalone.py
#     -touch-terrain-batch.sh <-generated batch script to run Touch Terrain
#   >touch_terrain_configs
#     -XX.json <-generated config JSON file for each state


# Run this file in geographic_data directory

# lower 48 us states
# resolution = 250

# oahu 5x
# resolution = 20

# usa48 low poly
# tifsPath = f'./globalLogScaleLandA/'

parser = argparse.ArgumentParser(description='touch terrain config generation')
parser.add_argument(
    'template', help='Path to template configuration that will be used.')
parser.add_argument('-gc', action='store_true')
parser.add_argument('-gt', action='store_true')
args = parser.parse_args()

templateWorkspace = './template-workspace/'
calcRasterBatchFilename = 'calcRaster-batch.sh'
clipRasterBatchFilename = 'clipRaster-batch.sh'
meshGenerationBatchFilename = 'meshGeneration-batch.sh'
meshBooleanBatchFilename = 'meshBoolean-batch.sh'

meshBooleanBin = './tools/gp-cli/precompiled/pc/bin/meshboolean.exe'


templateConfigurationPath = args.template


# use tt template config
# templateConfigurationPath = './touch_terrain_configuration_templates/individual-states.json'

templateRequiredKeys = [
    'templateName',
    'templateShortName',
    'parentTemplates',
    'demRes',
    'clipBoundariesDir',
    'rasterTypeSuffixes',
    'addResToPaths',
    'addSuffixToPaths',
    'excludeFileList',
    'targetSRS',
    '1mmToRealScale'
]
templateConfig = {}
templateName = ''
templateDEMRes = -1
if templateConfigurationPath:
    templateFp = open(templateConfigurationPath, 'r')
    templateConfig = json.load(templateFp)
    if isinstance(templateConfig, dict):
        for rK in templateRequiredKeys:
            if rK not in templateConfig:
                print(
                    f'Template - {templateConfigurationPath} is missing {rK}\n')
                sys.exit()

        def inheritFromParent(parentPath):
            pConfig = json.load(open(parentPath, 'r'))
            if isinstance(pConfig, dict):
                for pT in pConfig['parentTemplates']:
                    inheritFromParent(pT)
                for pK in pConfig.keys():
                    if pK not in templateConfig.keys():
                        templateConfig[pK] = pConfig[pK]

        for pT in templateConfig['parentTemplates']:
            inheritFromParent(pT)

        templateName = templateConfig['templateName']
        templateDEMRes = templateConfig['demRes']
        print(f'Loaded config template {templateName}')
        print(f'Using {len(templateConfig["calcRasterTypes"])} input paths')

    else:
        print(f'\nTemplate - {templateConfigurationPath} is not dict\n')
        sys.exit()


def clippedRastersPath(i):
    p = templateWorkspace + \
        templateConfig['templateShortName'] + '/' + \
        templateConfig['calcRasterTypes'][i]
    if templateConfig['addResToPaths']:
        p += '-' + str(templateDEMRes)
    if len(templateConfig['addSuffixToPaths']):
        p += templateConfig['addSuffixToPaths']
    p += '/'
    return p


print(f'Getting all file name listing from directory {clippedRastersPath(0)}')

configTemplatePath = f'./touch_terrain_configs/{templateConfig["templateShortName"]}/{templateDEMRes}/'

def delete_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except OSError:
        print("Error occurred while deleting files.")

# clip raster to boundaries
if args.gc:
    for i in range(0,len(templateConfig['calcRasterTypes'])):
        outputPath = clippedRastersPath(i)
        os.makedirs(os.path.dirname(outputPath), exist_ok=True) 
        print(f'Created directory {outputPath}')

    with open(f'{clipRasterBatchFilename}', 'w+') as cmdfp:
        cmdCount = 0
        for entry in os.scandir(templateConfig['clipBoundariesDir']):
            if entry.name.endswith('.gpkg') and entry.is_file():
                # print(entry.path)
                forwardSlashPath = entry.path.replace(os.sep, '/')

                entryName = entry.name.replace(".gpkg", "")

                if entryName in templateConfig['excludeFileList']:
                    continue
                
                print(entry)

                for i in range(0, len(templateConfig['calcRasterTypes'])):
                    clipRasterCmd = f'gdalwarp \
-overwrite \
-t_srs {templateConfig["targetSRS"]} \
-of GTiff \
-tr {str(templateDEMRes)} {str(templateDEMRes)} \
-cutline {forwardSlashPath} \
-crop_to_cutline \
{templateWorkspace}/{templateConfig["templateShortName"]}/{templateConfig["calcRasterTypes"][i]}-{str(templateDEMRes)}m.tif \
{clippedRastersPath(i)}{entryName}.tif \
-r near \
-multi \
-dstnodata -9999'
                    cmdfp.write(clipRasterCmd + '\n')
                    cmdCount += 1
        print(f'{cmdCount} clip command generated in {clipRasterBatchFilename}')

if args.gt:
    delete_files_in_directory(configTemplatePath)

    os.makedirs(os.path.dirname(configTemplatePath), exist_ok=True)
    print(f'Created directory {configTemplatePath}')

    print(os.path.basename(templateConfigurationPath).split(".")[0])

    outputSTLTopDir = './state_stls/'
    outputSTLTemplateDir = f'{outputSTLTopDir}{templateConfig["templateShortName"]}/{templateDEMRes}/'
    os.makedirs(os.path.dirname('./tmp/' + outputSTLTemplateDir), exist_ok=True)
    print(f'Created directory {"./tmp/" + outputSTLTemplateDir}')

    with open(f'{meshGenerationBatchFilename}', 'w+') as cmdGenfp, open(f'{meshBooleanBatchFilename}', 'w+') as cmdBoolfp:
        configFileCount = 0

        # use first path for master all file list
        # Process states by largest TIF first to optimize 3d model generation time
        # Small states should finish first and the larger states which need the most memoery will trickle in at the end.
        allFiles = os.listdir(clippedRastersPath(0))
        allFiles.sort(key=lambda f: os.stat(
            clippedRastersPath(0)+f).st_size, reverse=False)

        for entry in allFiles:
            if entry.endswith('.tif'):

                entryName = entry.replace(".tif", "")

                if entryName in templateConfig['excludeFileList']:
                    continue

                print(entry)

                # Get TIF extents to 3d print
                data = gdal.Open(
                    clippedRastersPath(0)+entry, GA_ReadOnly)
                geoTransform = data.GetGeoTransform()
                minx = geoTransform[0]
                maxy = geoTransform[3]
                maxx = minx + geoTransform[1] * data.RasterXSize
                miny = maxy + geoTransform[5] * data.RasterYSize
                # print([minx, miny, maxx, maxy])
                data = None

                # Create ttArgs dictionary to save to configuration json file
                # TouchTerrain_standalone.py should be run from the "geographic-data/state_stl" directory
                ttArgs = {
                    "importedDEM": '',
                    "DEM_name": 'USGS/NED',

                                "trlat": maxy,        # lat/lon of top right corner
                                "trlon": maxx,
                                "bllat": miny,        # lat/lon of bottom left corner
                                "bllon": minx,

                                # individual states
                                # width of each tile in mm (total width of TIF extent in meters divided by 500km = number of "200mm wide buildplates" needed at our 0.4mm = 1km scale)
                                # "tilewidth": 200 * ( maxx - minx ) / 500000,

                                # 5x size
                                # "tilewidth": 5*200 * ( maxx - minx ) / 500000,

                                # resolution (horizontal) of 3D printer (= size of one pixel) in mm
                                "printres": -1,

                                # oahu
                                # "basethick": 0, # thickness (in mm) of printed base

                                # individual states
                                # "basethick": 0.7, # thickness (in mm) of printed base
                                # "fill_holes": [-1, 7],
                                # "zscale": 5,      # elevation (vertical) scaling


                                # usa 48 state combined width 200mm buildplate is 5000km, 0.4mm = 10km
                                # "tilewidth": 200 * ( maxx - minx ) / 5000000,
                                # "printres": -1,
                                # "basethick": 5, # thickness (in mm) of printed base
                                # "zscale": 50,      # elevation (vertical) scaling
                                # "fill_holes": [-1, 8],

                                # USA 48 combined low poly
                                # 0.4mm = 10km
                                # "tilewidth": 200 * (maxx - minx) / 5000000,
                                # "printres": -1,
                                # thickness (in mm) of printed base
                                # "basethick": 2,
                                # "zscale": 100,      # elevation (vertical) scaling
                                # "fill_holes": [-1, 8],
                                # "ignore_leq": -100,
                                # "min_elev": -100,  # lowest point in NA is greater than -100m
                                # "smooth_borders": True,

                                # number of tiles in x and y. We are creating 1 big 3D model at our desired scale that we will custom divide to fit on the printer.
                                "ntilesx": 1,
                                "ntilesy": 1,



                                # indidivudal states
                                # "ignore_leq": -100,
                                # "min_elev": -100, #lowest point in NA is greater than -100m
                                # "smooth_borders": False,

                                # oahu
                                # "ignore_leq": -125,
                                # "min_elev": -125,
                                # "fill_holes": [-1, 7],


                                # format of 3D model files: "obj" wavefront obj (ascii),"STLa" ascii STL or "STLb" binary STL
                                "fileformat": "STLb",
                                # True-> all tiles are centered around 0/0, False, all tiles "fit together"
                                "tile_centered": False,
                                "zip_file_name": '',    # base name of zipfile, .zip will be added
                                # 0 means all cores, None (null in JSON!) => don't use multiprocessing
                                "CPU_cores_to_use": 0,
                                # if raster is bigger, use temp_files instead of memory
                                "max_cells_for_memory_only": 5000**2,
                                # "lower_leq": [1,0.3],
                                # "offset_masks_lower": [["./dems/stream-lake-mask-clipped-500m/" + entry, 1.7]],


                                "clean_diags": True
                }

                # overwrite args with template values
                for tK, tV in templateConfig.items():
                    if tK == '1mmToRealScale':
                        # (meters of real world)/((1mmtoRealScalemm)/(1000mmin1m))
                        ttArgs["tilewidth"] = (maxx - minx) / (tV / 1000)
                    elif tK in templateRequiredKeys:  # skip putting template metadata keys in the args passed to touchterrain
                        continue
                    else:
                        ttArgs[tK] = tV

                def generateZipFilenameForPathIndex(i):
                    return outputSTLTemplateDir + entryName + templateConfig['rasterTypeSuffixes'][i]

                for i in range(0, len(templateConfig['calcRasterTypes'])):
                    ttArgs["importedDEM"] = clippedRastersPath(i) + entry
                    ttArgs["zip_file_name"] = generateZipFilenameForPathIndex(
                        i)

                    configFilename = entryName + \
                        templateConfig['rasterTypeSuffixes'][i] + '.json'

                    with open(configTemplatePath + configFilename, 'w+') as fp:
                        json.dump(ttArgs, fp, indent=0, sort_keys=True)
                    configFileCount += 1

                    cmdGenfp.write(
                        f'python ./TouchTerrain_standalone.py {configTemplatePath + configFilename}' + '\n')

                if len(templateConfig['calcRasterTypes']) >= 2:
                    # Write libigl gp-CLI command for boolean subtract between second and first STL
                    cmdBoolfp.write(f'echo {configFileCount} Mesh boolean subtracting {entryName}' + '\n' +
                                    f'time {meshBooleanBin} {generateZipFilenameForPathIndex(1)}/{entryName}_tile_1_1.STL {generateZipFilenameForPathIndex(0)}/{entryName}_tile_1_1.STL minus {generateZipFilenameForPathIndex(0)}/{entryName}_rivers.STL' + '\n' + f'echo {entryName} result $?' + '\n')

                if len(templateConfig['calcRasterTypes']) >= 2:
                    # Write libigl gp-CLI command for boolean subtract between second and third STL
                    cmdBoolfp.write(f'echo {configFileCount} Mesh boolean subtracting {entryName}' + '\n' +
                                    f'time {meshBooleanBin} {generateZipFilenameForPathIndex(1)}/{entryName}_tile_1_1.STL {generateZipFilenameForPathIndex(2)}/{entryName}_tile_1_1.STL minus {generateZipFilenameForPathIndex(2)}/{entryName}_thru_rivers.STL' + '\n' + f'echo {entryName} result $?' + '\n')

        print(
            f'Wrote {str(configFileCount)} config files to {configTemplatePath}')


    print(f'{meshGenerationBatchFilename} should be run from {os.getcwd()}')

    print(
        f'Each state will be unzipped into its own folder in {outputSTLTopDir} relative to where batch file is run from.')
    print('Run libigl-boolean-subtract.sh after generating 3d state stls to perform boolean subtract to create rivers only 3d model')
    print('Ex: \nchmod 700 touch-terrain-batch.sh\n./touch-terrain-batch.sh\nnice -n 5 ./libigl-boolean-subtract.sh')


    print('\nClean up nonmanifold meshes afterward with blender 3d print toolbox.')
