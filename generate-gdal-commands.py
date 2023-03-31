import os
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

#boundaryScanDir = "./cb_2018_us_state_20m_individual"
boundaryScanDir = "./tl_2022_us_state/split_individual/"

gdalwarpBatchFilename = 'gdalwarp-batch.sh'
#gdalcalcBatchFilename = 'gdalcalc-batch.sh'

resolution = 500 #200
raised = 460 #160
hydroPatchedRaised = 400 #100

with open('./'+gdalwarpBatchFilename, 'w+') as cmdfp:
    
    #calcCmdfp = open('./'+gdalcalcBatchFilename, 'w+')
    
    commandCount = 0
    
    for entry in os.scandir(boundaryScanDir):
    	if entry.name.endswith('.gpkg') and entry.is_file():
    		#print(entry.path)
            forwardSlashPath = entry.path.replace(os.sep, '/')
            
            stateName = entry.name.replace(".gpkg","")
    
            clipElevationCmd = f'gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr {resolution} {resolution} -tap -cutline {forwardSlashPath} -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-{resolution}m-width-raised-{raised}.tif ./dems/7-5-arc-second-clipped-{resolution}m/{stateName}.tif -r cubicspline -multi -dstnodata -9999'

            clipElevationRaisedHydroCmd = f'gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr {resolution} {resolution} -tap -cutline {forwardSlashPath} -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-{resolution}m-width-hydro-patched-raised-{hydroPatchedRaised}.tif C:/Users/ansonl/development/dem-to-stl-workflow/dems/7-5-arc-second-clipped-{resolution}m-hydro-patched/{stateName}-hydro-patched.tif -r cubicspline -multi'
            
            #calcLeq0Cmd = f'python gdal_calc.py -A ./dems/7-5-arc-second-clipped-500m/{stateName}.tif --outfile ./dems/7-5-arc-second-clipped-500m/{stateName}.tif --calc="A*(A>0)+(A<0)*1"'
    
            commandCount += 2
            cmdfp.write(clipElevationCmd + '\n')
            #cmdfp.write(clipHydroMaskCmd + '\n')
            cmdfp.write(clipElevationRaisedHydroCmd + '\n')
            
            #calcCmdfp.write(calcLeq0Cmd + '\n')

print('Wrote ' + str(commandCount) + ' commands to ' + gdalwarpBatchFilename)

print(f'{gdalwarpBatchFilename} should be run from root project folder\n\nEx: \nchmod 700 {gdalwarpBatchFilename}\n./{gdalwarpBatchFilename}')
    
