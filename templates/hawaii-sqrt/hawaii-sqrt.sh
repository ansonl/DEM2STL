#run this script from within the directory TOPDIR/template-workspace/TEMPLATE/RES/

#PATH setup
$env:TOPDIR = '../../../'

$env:PYTHONPATH = "$env:TOPDIR/templates/hawaii-sqrt/"
$env:PATCHVRTPATH = "$env:TOPDIR/workflow/patchVRT.py"

$env:SOURCES = "$env:TOPDIR/sources/Hawaii"
$env:HYDROGRAPHICMASKS = "$env:TOPDIR/hydrographic-masks/"

#create VRT for globalScaleLandA
gdalbuildvrt -resolution highest -overwrite globalScaleLandA.vrt $env:SOURCES/hawaii_gmted2010_strm_merge_32604_200m_50m_cubicspline.tif
python $env:PATCHVRTPATH globalScaleLandA.vrt globalScaleLandA
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" globalScaleLandA.vrt globalScaleLandA.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for raiseLandAIfNotInHydroMaskBAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAIfNotInHydroMaskBAndScale.vrt globalScaleLandA.tif $env:SOURCES/coastline_mask_32604_250m.tif
python $env:PATCHVRTPATH raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 250 250 raiseLandAIfNotInHydroMaskBAndScale.tif raiseLandAIfNotInHydroMaskBAndScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for raiseLandAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAScale.vrt globalScaleLandA.tif $env:SOURCES/coastline_mask_32604_250m.tif
python $env:PATCHVRTPATH raiseLandAScale.vrt raiseLandAAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAScale.vrt raiseLandAScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 250 250 raiseLandAScale.tif raiseLandAScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for deleteLandAIfInHydroMaskB (translucent DEM)
gdalbuildvrt -resolution highest -overwrite deleteLandAIfInHydroMaskB.vrt ./raiseLandAIfNotInHydroMaskBAndScale.tif $env:SOURCES//coastline_mask_32604_250m.tif
python $env:PATCHVRTPATH deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 250 250 deleteLandAIfInHydroMaskB.tif deleteLandAIfInHydroMaskB_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for keepLandAIfNotInHydroMaskB (single print DEM)
gdalbuildvrt -resolution highest -overwrite keepLandAIfNotInHydroMaskB.vrt globalScaleLandA.tif $env:SOURCES//coastline_mask_32604_250m.tif
python $env:PATCHVRTPATH keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 250 250 keepLandAIfNotInHydroMaskB.tif keepLandAIfNotInHydroMaskB_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#gdal
#python ./generate-batch.py .\templates\hawaii-sqrt\hawaii-sqrt.json -gc


#tt
#python ./generate-batch.py .\templates\hawaii-sqrt\hawaii-sqrt.json -gt

#run from top dir
python ./TouchTerrain_standalone.py ./template-workspace/hawaii-sqrt/250//touch_terrain_configs/HI.json
python ./TouchTerrain_standalone.py ./template-workspace/hawaii-sqrt/250//touch_terrain_configs/HI-no-rivers.json
python ./TouchTerrain_standalone.py ./template-workspace/hawaii-sqrt/250//touch_terrain_configs/HI-thru-river-cutout-base.json
python ./TouchTerrain_standalone.py ./template-workspace/hawaii-sqrt/250//touch_terrain_configs/HI-single-print.json

#run from top dir
echo 6 Mesh boolean subtracting HI
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/hawaii-sqrt/250/HI-no-rivers/raiseLandAScale_tap_tile_1_1.STL ./state_stls/hawaii-sqrt/250/HI/raiseLandAIfNotInHydroMaskBAndScale_tap_tile_1_1.STL minus ./state_stls/hawaii-sqrt/250/HI/HI_rivers.STL
echo HI result $?
echo 7 Mesh boolean subtracting HI
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/hawaii-sqrt/250/HI-no-rivers/raiseLandAScale_tap_tile_1_1.STL ./state_stls/hawaii-sqrt/250/HI-thru-river-cutout-base/deleteLandAIfInHydroMaskB_tap_tile_1_1.STL minus ./state_stls/hawaii-sqrt/250/HI-thru-river-cutout-base/HI_thru_rivers.STL
echo HI result $?