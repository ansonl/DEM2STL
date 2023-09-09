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
templateConfigurationPath = parser.parse_args().template


# use tt template config
# templateConfigurationPath = './touch_terrain_configuration_templates/individual-states.json'

templateRequiredKeys = ['templateName', 'parentTemplates', 'demRes',
                        'pathsAndOutputFileSuffix', 'addResToPaths', 'addSuffixToPaths', 'excludeFileList', '1mmToRealScale']
templateConfig = {}
templateName = ''
templateDEMRes = -1
templatePathsAndOutputFileSuffix = []
if templateConfigurationPath:
    templateFp = open(templateConfigurationPath, 'r')
    templateConfig = json.load(templateFp)
    if isinstance(templateConfig, dict):
        for rK in templateRequiredKeys:
            if rK not in templateConfig:
                print(
                    f'Template - {templateConfigurationPath} is missing {templateRequiredKeys}\n')
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
        templatePathsAndOutputFileSuffix = templateConfig['pathsAndOutputFileSuffix']
        for i in range(0, len(templatePathsAndOutputFileSuffix)):
            if templateConfig['addResToPaths']:
                templatePathsAndOutputFileSuffix[i][0] += str(templateDEMRes)
            if len(templateConfig['addSuffixToPaths']):
                templatePathsAndOutputFileSuffix[i][0] += templateConfig['addSuffixToPaths']
        print(f'Loaded config template {templateName}')
        print(f'Using {len(templatePathsAndOutputFileSuffix)} input paths')
        print(
            f'Getting all file name listing from directory {templatePathsAndOutputFileSuffix[0][0]}')
    else:
        print(f'\nTemplate - {templateConfigurationPath} is not dict\n')
        sys.exit()

configTemplatePath = f'./touch_terrain_configs/{os.path.basename(templateConfigurationPath).split(".")[0]}/{templateDEMRes}/'
def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
   except OSError:
     print("Error occurred while deleting files.")
delete_files_in_directory(configTemplatePath)

os.makedirs(os.path.dirname(configTemplatePath), exist_ok=True)

print(os.path.basename(templateConfigurationPath).split(".")[0])

outputSTLTopDir = './state_stls/'
outputSTLTemplateDir = f'{outputSTLTopDir}{os.path.basename(templateConfigurationPath).split(".")[0]}/{templateDEMRes}/'
os.makedirs(os.path.dirname('./tmp/' + outputSTLTemplateDir), exist_ok=True)

with open('./touch-terrain-batch.sh', 'w+') as cmdfp:

    libiglcmdfp = open('./libigl-boolean-subtract.sh', 'w+')
    configFileCount = 0

    # use first path for master all file list
    # Process states by largest TIF first to optimize 3d model generation time
    # Small states should finish first and the larger states which need the most memoery will trickle in at the end.
    allFiles = os.listdir(templatePathsAndOutputFileSuffix[0][0])
    allFiles.sort(key=lambda f: os.stat(
        templatePathsAndOutputFileSuffix[0][0]+f).st_size, reverse=False)

    for entry in allFiles:
        if entry.endswith('.tif'):

            entryName = entry.replace(".tif", "")

            if entryName in templateConfig['excludeFileList']:
                continue

            print(entry)

            # Get TIF extents to 3d print
            data = gdal.Open(
                templatePathsAndOutputFileSuffix[0][0]+entry, GA_ReadOnly)
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
                return outputSTLTemplateDir + entryName + templatePathsAndOutputFileSuffix[i][1]

            for i in range(0, len(templatePathsAndOutputFileSuffix)):
                ttArgs["importedDEM"] = templatePathsAndOutputFileSuffix[i][0] + entry
                ttArgs["zip_file_name"] = generateZipFilenameForPathIndex(i)

                configFilename = entryName + \
                    templatePathsAndOutputFileSuffix[i][1] + '.json'

                with open(configTemplatePath + configFilename, 'w+') as fp:
                    json.dump(ttArgs, fp, indent=0, sort_keys=True)
                configFileCount += 1

                cmdfp.write(
                    f'python ./TouchTerrain_standalone.py {configTemplatePath + configFilename}' + '\n')

            if len(templatePathsAndOutputFileSuffix) >= 2:
                # Write libigl gp-CLI command for boolean subtract between second and first STL
                libiglcmdfp.write(f'echo {configFileCount} Mesh boolean subtracting {entryName}' + '\n' +
                                  f'time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe {generateZipFilenameForPathIndex(1)}/{entryName}_tile_1_1.STL {generateZipFilenameForPathIndex(0)}/{entryName}_tile_1_1.STL minus {generateZipFilenameForPathIndex(0)}/{entryName}_rivers.STL' + '\n' + f'echo {entryName} result $?' + '\n')

            if len(templatePathsAndOutputFileSuffix) >= 3:
                # Write libigl gp-CLI command for boolean subtract between second and third STL
                libiglcmdfp.write(f'echo {configFileCount} Mesh boolean subtracting {entryName}' + '\n' +
                                  f'time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe {generateZipFilenameForPathIndex(1)}/{entryName}_tile_1_1.STL {generateZipFilenameForPathIndex(2)}/{entryName}_tile_1_1.STL minus {generateZipFilenameForPathIndex(2)}/{entryName}_thru_rivers.STL' + '\n' + f'echo {entryName} result $?' + '\n')

libiglcmdfp.close()

print(f'Wrote {str(configFileCount)} config files to {configTemplatePath}')

print(f'touch-terrain-batch.sh should be run from {os.getcwd()}')

print(
    f'Each state will be unzipped into its own folder in {outputSTLTopDir} relative to where batch file is run from.')
print('Run libigl-boolean-subtract.sh after generating 3d state stls to perform boolean subtract to create rivers only 3d model')
print('Ex: \nchmod 700 touch-terrain-batch.sh\n./touch-terrain-batch.sh\nnice -n 5 ./libigl-boolean-subtract.sh')


print('\nClean up nonmanifold meshes afterward with blender 3d print toolbox.')
