import os
import gdal
from gdalconst import GA_ReadOnly
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
os.chdir("./state_stls")

with open('./touch-terrain-batch.sh', 'w+') as cmdfp:
    os.chdir("../dems/1000m-clipped")
    
    configFileCount = 0
    
    for entry in os.scandir("."):
    	if entry.name.endswith('.tif') and entry.is_file():
    		#print(entry.path)
    
    		# Get TIF extents to 3d print
    		data = gdal.Open(entry.path, GA_ReadOnly)
    		geoTransform = data.GetGeoTransform()
    		minx = geoTransform[0]
    		maxy = geoTransform[3]
    		maxx = minx + geoTransform[1] * data.RasterXSize
    		miny = maxy + geoTransform[5] * data.RasterYSize
    		#print([minx, miny, maxx, maxy])
    		data = None
    
    		# Create args dictionary to save to configuration json file
    		# TouchTerrain_standalone.py should be run from the "geographic-data/state_stl" directory
    		args = {
    			"importedDEM": "../dems/1000m-clipped/" + entry.name,
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
    	        "basethick": 1, # thickness (in mm) of printed base
    	        "zscale": 5,      # elevation (vertical) scaling
    
    	        "fileformat": "STLb",  # format of 3D model files: "obj" wavefront obj (ascii),"STLa" ascii STL or "STLb" binary STL
    	        "tile_centered": False, # True-> all tiles are centered around 0/0, False, all tiles "fit together"
    	        "zip_file_name": entry.name.replace(".tif",""),   # base name of zipfile, .zip will be added
    	        "CPU_cores_to_use" : 0,  # 0 means all cores, None (null in JSON!) => don't use multiprocessing
    	        "max_cells_for_memory_only" : 5000^2, # if raster is bigger, use temp_files instead of memory
    	    }
    
    		configFilename = entry.name.replace(".tif","")+'.json'
            
    		configsPath = '../../touch_terrain_configs/'
    		with open(configsPath + configFilename, 'w+') as fp:
    			json.dump(args, fp, indent=0, sort_keys=True)
    			configFileCount += 1
            
    		cmdfp.write('python ./TouchTerrain_standalone.py ../touch_terrain_configs/' + configFilename + '\n')

print('Wrote ' + str(configFileCount) + ' config files to ' + configsPath)

print('touch-terrain-batch.sh should be run from ./geographic-data folder\n\nEx: \nchmod 700 touch-terrain-batch.sh\n./touch-terrain-batch.sh')

print('\n\nEach state will be unzipped into its own folder where batch file is run from.')
    
