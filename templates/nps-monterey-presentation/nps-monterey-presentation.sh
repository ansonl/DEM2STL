#run this script from within the directory TOPDIR/template-workspace/TEMPLATE/RES/

# cd .\development\dem-to-stl-workflow\template-workspace\nps-monterey-presentation\30

#PATH setup
$env:TOPDIR = '../../../'

$env:PYTHONPATH = "$env:TOPDIR/templates/nps-monterey-presentation/"
$env:PATCHVRTPATH = "$env:TOPDIR/workflow/patchVRT.py"

$env:SOURCES = "$env:TOPDIR/sources/"
$env:HYDROGRAPHICMASKS = "$env:TOPDIR/hydrographic-masks/"
${env:MONTEREY-SOURCES} = "$env:TOPDIR/../maps/nps-presentation/"

#create VRT for raiseLandAByBAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAByBAndScale.vrt ${env:MONTEREY-SOURCES}/Monterey-SRTM-UTM10N.tif ${env:MONTEREY-SOURCES}/Monterey-NVDI-point25-point7-100times-int16.tif
python $env:PATCHVRTPATH raiseLandAByBAndScale.vrt raiseLandAByBAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAByBAndScale.vrt raiseLandAByBAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 30 30 raiseLandAByBAndScale.tif raiseLandAByBAndScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for raiseLandAByBAndScaleB5Version
gdalbuildvrt -resolution highest -overwrite raiseLandAByBAndScaleB5Version.vrt ${env:MONTEREY-SOURCES}/Monterey-SRTM-UTM10N.tif ${env:MONTEREY-SOURCES}/Monterey-landsat-b5-point27-times100-int16.tif
python $env:PATCHVRTPATH raiseLandAByBAndScaleB5Version.vrt raiseLandAByBAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAByBAndScaleB5Version.vrt raiseLandAByBAndScaleB5Version.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 30 30 raiseLandAByBAndScaleB5Version.tif raiseLandAByBAndScaleB5Version_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for raiseLandAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAAndScale.vrt ${env:MONTEREY-SOURCES}/Monterey-SRTM-UTM10N.tif
python $env:PATCHVRTPATH raiseLandAAndScale.vrt raiseLandAAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAAndScale.vrt raiseLandAAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 30 30 raiseLandAAndScale.tif raiseLandAAndScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#clip
gdalwarp -overwrite -of GTiff -tr 30 30 -cutline ${env:MONTEREY-SOURCES}/clip.gpkg -crop_to_cutline raiseLandAByBAndScale_tap.tif raiseLandAByBAndScale_tap/NP.tif -r near -multi -dstnodata -9999 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"
gdalwarp -overwrite -of GTiff -tr 30 30 -cutline ${env:MONTEREY-SOURCES}/clip.gpkg -crop_to_cutline raiseLandAByBAndScaleB5Version_tap.tif raiseLandAByBAndScaleB5Version_tap/NP.tif -r near -multi -dstnodata -9999 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"
gdalwarp -overwrite -of GTiff -tr 30 30 -cutline ${env:MONTEREY-SOURCES}/clip.gpkg -crop_to_cutline raiseLandAAndScale_tap.tif raiseLandAAndScale_tap/NP.tif -r near -multi -dstnodata -9999 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#tt
python ./generate-batch.py .\templates\nps-monterey-presentation\nps-monterey-presentation.json -gt

python ./TouchTerrain_standalone.py ./template-workspace/nps-monterey-presentation/30//touch_terrain_configs/NP.json
python ./TouchTerrain_standalone.py ./template-workspace/nps-monterey-presentation/30//touch_terrain_configs/NP-no-rivers.json
python ./TouchTerrain_standalone.py ./template-workspace/nps-monterey-presentation/30//touch_terrain_configs/NP-b5.json

time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/nps-monterey-presentation/30/NP/NP_tile_1_1.STL ./state_stls/nps-monterey-presentation/30/NP-no-rivers/NP_tile_1_1.STL minus ./state_stls/nps-monterey-presentation/30/NP/NP_rivers.STL

time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/nps-monterey-presentation/30/NP-b5/NP_tile_1_1.STL ./state_stls/nps-monterey-presentation/30/NP-no-rivers/NP_tile_1_1.STL minus ./state_stls/nps-monterey-presentation/30/NP/NP_rivers-b5.STL