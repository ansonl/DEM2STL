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
boundaryScanDir = "./sources/USCB/tl_2022_us_state/split_individual/"

gdalwarpBatchFilename = 'gdalwarp-batch.sh'
#gdalcalcBatchFilename = 'gdalcalc-batch.sh'

resolution = 250 #200
raised = 460 #160
hydroPatchedRaised = 400 #100

destPath1 = f'C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/raiseLandAIfNotInHydroMaskBAndScaleAt4m-{resolution}m-clipped/'
destPath2 = f'C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/raiseLandAScaleAt4m-{resolution}m-clipped/'

with open('./'+gdalwarpBatchFilename, 'w+') as cmdfp:
    
    #calcCmdfp = open('./'+gdalcalcBatchFilename, 'w+')
    
    commandCount = 0
    
    for entry in os.scandir(boundaryScanDir):
    	if entry.name.endswith('.gpkg') and entry.is_file():
    		#print(entry.path)
            forwardSlashPath = entry.path.replace(os.sep, '/')
            
            stateName = entry.name.replace(".gpkg","")
    
            clipElevationCmd = f'gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr {resolution} {resolution} -cutline {forwardSlashPath} -crop_to_cutline ./dem-feature-generation/raiseLandAIfNotInHydroMaskBAndScaleAt4m-{resolution}m-raised-{raised}m.tif {destPath1}{stateName}.tif -r near -multi -dstnodata -9999'

            clipElevationRaisedHydroCmd = f'gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr {resolution} {resolution} -cutline {forwardSlashPath} -crop_to_cutline ./dem-feature-generation/raiseLandAScaleAt4m-{resolution}m-raised-{hydroPatchedRaised}m.tif {destPath2}{stateName}.tif -r near -multi'
            
            #calcLeq0Cmd = f'python gdal_calc.py -A ./dems/7-5-arc-second-clipped-500m/{stateName}.tif --outfile ./dems/7-5-arc-second-clipped-500m/{stateName}.tif --calc="A*(A>0)+(A<0)*1"'
    
            commandCount += 2
            cmdfp.write(clipElevationCmd + '\n')
            #cmdfp.write(clipHydroMaskCmd + '\n')
            cmdfp.write(clipElevationRaisedHydroCmd + '\n')
            
            #calcCmdfp.write(calcLeq0Cmd + '\n')

print('Wrote ' + str(commandCount) + ' commands to ' + gdalwarpBatchFilename)

print(f'{gdalwarpBatchFilename} should be run from root project folder\n\nEx: \nchmod 700 {gdalwarpBatchFilename}\n./{gdalwarpBatchFilename}')
    
