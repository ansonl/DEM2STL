#run this script from within the directory TOPDIR/template-workspace/TEMPLATE/RES/

#PATH setup
$env:TOPDIR = '../../../'

$env:PYTHONPATH = "$env:TOPDIR/templates/cn-asia-conformal-conic-sqrt/"
$env:PATCHVRTPATH = "$env:TOPDIR/workflow/patchVRT.py"

$env:SOURCES = "$env:TOPDIR/sources/"
$env:HYDROGRAPHICMASKS = "./"
${env:CHINA-SOURCES} = "$env:TOPDIR/../maps/china/"

#use sources from cn-linear map

#run below in template workspace

#create VRT for globalScaleLandA
gdalbuildvrt -resolution highest -overwrite globalScaleLandA.vrt ${env:CHINA-SOURCES}/cn-gmted-srtm-merge-102027-4000m-avg-1000m-cubicspline.tif
python $env:PATCHVRTPATH globalScaleLandA.vrt globalScaleLandA
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" globalScaleLandA.vrt globalScaleLandA.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for raiseLandAIfNotInHydroMaskBAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAIfNotInHydroMaskBAndScale.vrt globalScaleLandA.tif ${env:CHINA-SOURCES}/cn-hydrographic-mask-merge-102027-1000m.tif
python $env:PATCHVRTPATH raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 1000 1000 raiseLandAIfNotInHydroMaskBAndScale.tif raiseLandAIfNotInHydroMaskBAndScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for raiseLandAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAAndScale.vrt globalScaleLandA.tif
python $env:PATCHVRTPATH raiseLandAAndScale.vrt raiseLandAAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAAndScale.vrt raiseLandAAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 1000 1000 raiseLandAAndScale.tif raiseLandAAndScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for deleteLandAIfInHydroMaskB (translucent DEM)
gdalbuildvrt -resolution highest -overwrite deleteLandAIfInHydroMaskB.vrt ./raiseLandAIfNotInHydroMaskBAndScale.tif ${env:CHINA-SOURCES}/cn-hydrographic-mask-merge-102027-1000m.tif
python $env:PATCHVRTPATH deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 1000 1000 deleteLandAIfInHydroMaskB.tif deleteLandAIfInHydroMaskB_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for keepLandAIfNotInHydroMaskB (single print DEM)
gdalbuildvrt -resolution highest -overwrite keepLandAIfNotInHydroMaskB.vrt globalScaleLandA.tif ${env:CHINA-SOURCES}/cn-hydrographic-mask-merge-102027-1000m.tif
python $env:PATCHVRTPATH keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 1000 1000 keepLandAIfNotInHydroMaskB.tif keepLandAIfNotInHydroMaskB_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#gdal
python ./generate-batch.py .\templates\cn-asia-conformal-conic-sqrt\cn-asia-conformal-conic-sqrt.json -gc

#run generated gdal commands

#tt
python ./generate-batch.py .\templates\cn-asia-conformal-conic-sqrt\cn-asia-conformal-conic-sqrt.json -gt

#run tt from top dir
python ./TouchTerrain_standalone.py ./template-workspace/cn-asia-conformal-conic-sqrt/1000//touch_terrain_configs/CN.json
python ./TouchTerrain_standalone.py ./template-workspace/cn-asia-conformal-conic-sqrt/1000//touch_terrain_configs/CN-no-rivers.json
python ./TouchTerrain_standalone.py ./template-workspace/cn-asia-conformal-conic-sqrt/1000//touch_terrain_configs/CN-thru-river-cutout-base.json
python ./TouchTerrain_standalone.py ./template-workspace/cn-asia-conformal-conic-sqrt/1000//touch_terrain_configs/CN-single-print.json