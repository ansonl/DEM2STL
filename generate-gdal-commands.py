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


# Run this file in root project directory
#os.chdir("./cb_2019_us_states_individual")

batchFilename = 'gdal-batch.sh'

with open('./'+batchFilename, 'w+') as cmdfp:
    
    commandCount = 0
    
    for entry in os.scandir("./cb_2019_us_state_500k_individual"):
    	if entry.name.endswith('.gpkg') and entry.is_file():
    		#print(entry.path)
            
            stateName = entry.name.replace(".gpkg","")
    
            clipElevationCmd = f'gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline {entry.path} -crop_to_cutline ./dems/30-arc-second-merged.tif ./dems/7-5-arc-second-clipped-500m/{stateName}.tif -r cubic -multi'

            clipMaskCmd = f'gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline {entry.path} -crop_to_cutline ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_merged_100m.tif C:/Users/ansonl/development/dem-to-stl-workflow/dems/stream-lake-mask-clipped-500m/{stateName}.tif -r cubic -multi'
    
            commandCount += 2
            cmdfp.write(clipElevationCmd + '\n')
            cmdfp.write(clipMaskCmd + '\n')

print('Wrote ' + str(commandCount) + ' commands to ' + batchFilename)

print(f'{batchFilename} should be run from root project folder\n\nEx: \nchmod 700 {batchFilename}\n./{batchFilename}')
    
