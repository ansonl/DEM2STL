import os
# Set imports based on environment and packages
#import gdal
#from gdalconst import GA_ReadOnly
from osgeo import gdal
from osgeo import gdalconst
from osgeo.gdalconst import GA_ReadOnly

import json

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

resolution = 250

#tifsPath = "./dems/7-5-arc-second-clipped-500m/"
#tifsPath2 = "./dems/7-5-arc-second-clipped-500m-hydro-patched/"
tifsPath = f'./dem-feature-generation/raiseLandAIfNotInHydroMaskBAndScaleAt4m-{resolution}m-clipped/'
tifsPath2 = f'./dem-feature-generation/raiseLandAScaleAt4m-{resolution}m-clipped/'
outputSTLTopDir = f'./state_stls_{resolution}m/'

with open('./touch-terrain-batch.sh', 'w+') as cmdfp:
    
    libiglcmdfp = open('./libigl-boolean-subtract.sh', 'w+')
    configFileCount = 0
    
    # Process states by largest TIF first to optimize 3d model generation time
    # Small states should finish first and the larger states which need the most memoery will trickle in at the end.
    allFiles = os.listdir(tifsPath)
    allFiles.sort(key=lambda f: os.stat(tifsPath+f).st_size, reverse=False)
    
    for entry in allFiles:
        if entry.endswith('.tif'):
            #print(entry.path)
            entryName = entry.replace(".tif","")
            entryPath = tifsPath + entry
    
            # Get TIF extents to 3d print
            data = gdal.Open(tifsPath+entry, GA_ReadOnly)
            geoTransform = data.GetGeoTransform()
            minx = geoTransform[0]
            maxy = geoTransform[3]
            maxx = minx + geoTransform[1] * data.RasterXSize
            miny = maxy + geoTransform[5] * data.RasterYSize
            #print([minx, miny, maxx, maxy])
            data = None
    
            zipFilename1 = outputSTLTopDir + entryName
    
            # Create args dictionary to save to configuration json file
            # TouchTerrain_standalone.py should be run from the "geographic-data/state_stl" directory
            args = {
                "importedDEM": entryPath,
                "DEM_name": 'USGS/NED',
    
                "trlat": maxy,        # lat/lon of top right corner
                "trlon": maxx,
                "bllat": miny,        # lat/lon of bottom left corner
                "bllon": minx,
    
                # width of each tile in mm (total width of TIF extent in meters divided by 500km = number of "200mm wide buildplates" needed at our 0.4mm = 1km scale)
                "tilewidth": 200 * ( maxx - minx ) / 500000, 
                
                # number of tiles in x and y. We are creating 1 big 3D model at our desired scale that we will custom divide to fit on the printer.
                "ntilesx": 1,
                "ntilesy": 1,
    
                "printres": -1,  # resolution (horizontal) of 3D printer (= size of one pixel) in mm
                "smooth_borders": False,
                "ignore_leq": 0,
                "basethick": 0.5, # thickness (in mm) of printed base
                "zscale": 5,      # elevation (vertical) scaling
    
                "fileformat": "STLb",  # format of 3D model files: "obj" wavefront obj (ascii),"STLa" ascii STL or "STLb" binary STL
                "tile_centered": False, # True-> all tiles are centered around 0/0, False, all tiles "fit together"
                "zip_file_name": zipFilename1,    # base name of zipfile, .zip will be added
                "CPU_cores_to_use" : 0,  # 0 means all cores, None (null in JSON!) => don't use multiprocessing
                "max_cells_for_memory_only" : 5000**2, # if raster is bigger, use temp_files instead of memory
                #"lower_leq": [1,0.3],
                #"offset_masks_lower": [["./dems/stream-lake-mask-clipped-500m/" + entry, 1.7]],
                "fill_holes": [-1, 7],
                "min_elev": 0,
                "clean_diags": True
            }
    
            configFilename = entry.replace(".tif","")+'.json'
            
            # Write config for STL with rivers "lowered"
            configsPath = f'./touch_terrain_configs_{resolution}m/'
            with open(configsPath + configFilename, 'w+') as fp:
                json.dump(args, fp, indent=0, sort_keys=True)
                configFileCount += 1
            
            cmdfp.write(f'python ./TouchTerrain_standalone.py ./touch_terrain_configs_{resolution}m/' + configFilename + '\n')
            
            # Write config for STL without rivers but with max height, slightly (0.1mm) lower than previous file
            args["importedDEM"] = tifsPath2 + entry.replace(".tif",".tif")
            args["basethick"] = args["basethick"] #- 0.1 #decrease base thickness by 0.1mm if hydro patched DEM is not already artificially lowered by 50m
            #args.pop("offset_masks_lower")
            zipFilename2 = outputSTLTopDir + entryName + "-no-rivers"
            args["zip_file_name"] = zipFilename2
            configFilename = entryName + "-no-rivers" +'.json'
            configsPath = f'./touch_terrain_configs_{resolution}m/'
            with open(configsPath + configFilename, 'w+') as fp:
                json.dump(args, fp, indent=0, sort_keys=True)
                configFileCount += 1
                
            # Write libigl gp-CLI command for boolean subtract between second and first STL
            libiglcmdfp.write(f'echo Mesh boolean subtracting {entryName}' + '\n' + f'time ./gp-cli/precompiled/pc/bin/meshboolean.exe {zipFilename2}/{entryName}-hydro-patched_tile_1_1.STL {zipFilename1}/{entryName}_tile_1_1.STL minus {zipFilename1}/{entryName}_rivers.STL' + '\n' + f'echo {entryName} result $?' + '\n')
            
            cmdfp.write(f'python ./TouchTerrain_standalone.py ./touch_terrain_configs_{resolution}m/' + configFilename + '\n')

libiglcmdfp.close()

print('Wrote ' + str(configFileCount) + ' config files to ' + configsPath)

print('touch-terrain-batch.sh should be run from ./geographic-data folder\n\nEx: \nchmod 700 touch-terrain-batch.sh\n./touch-terrain-batch.sh')

print('\n\nEach state will be unzipped into its own folder where batch file is run from.')

print('\n\nRun nice -n 5 ./libigl-boolean-subtract.sh after generating 3d state stls to perform boolean subtract to create rivers only 3d model. ')
print('\nClean up nonmanifold meshes with blender 3d print toolbox.')
    
os.chdir("./../../")