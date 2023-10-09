#run this script from within the directory TOPDIR/template-workspace/TEMPLATE/RES/

#PATH setup
$env:TOPDIR = '../../../'

$env:PYTHONPATH = "$env:TOPDIR/templates/cn-asia-conformal-conic-linear/"
$env:PATCHVRTPATH = "$env:TOPDIR/workflow/patchVRT.py"

$env:SOURCES = "$env:TOPDIR/sources/"
$env:HYDROGRAPHICMASKS = "./"
${env:CHINA-SOURCES} = "$env:TOPDIR/../maps/china/"

#run in ${env:CHINA-SOURCES}
cd ${env:CHINA-SOURCES}
#hydrographic mask preparation
#merge hydro1k, hydrolakes masks
gdalbuildvrt -resolution highest -overwrite cn-hydrographic-mask-merge.vrt cn-hydrolakes-025deg-wgs84.tif cn-hydro1k-buffered-4000m-025deg-wgs84.tif 
#reproject to 102027 and downscale to 1000x1000m
#did this by saving merged vrt in QGIS to avoid errors
gdalwarp -overwrite -t_srs ESRI:102027 -tr 1000.0 1000.0 cn-hydrographic-mask-merge.vrt cn-hydrographic-mask-merge-102027-1000m.vrt -r max -multi -co "TILED=YES" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" cn-hydrographic-mask-merge-102027-1000m.vrt cn-hydrographic-mask-merge-102027-1000m.tif

#Source DEM processing
#crop srtm to PRC boundary
#done in QGIS
#reproject dem to 102027 and downscale to 4000x4000m(avg)
gdalwarp -overwrite -t_srs ESRI:102027 -tr 4000.0 4000.0 cn-gmted-srtm-merge-clipped.tif cn-gmted-srtm-merge-clipped-102027-4000m.vrt -r average -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
#reproject to 102027 and upscale to 1000x1000m(cubicspline) For expected print res at 2000x2000m.
gdalwarp -overwrite -t_srs ESRI:102027 -tr 1000.0 1000.0 cn-gmted-srtm-merge-clipped-102027-4000m.vrt cn-gmted-srtm-merge-clipped-102027-4000m-1000m.vrt -r cubic -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" cn-gmted-srtm-merge-clipped-102027-4000m-1000m.vrt cn-gmted-srtm-merge-102027-4000m-avg-1000m-cubicspline.tif

#run below in template workspace
#create VRT for raiseLandAIfNotInHydroMaskBAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAIfNotInHydroMaskBAndScale.vrt ${env:CHINA-SOURCES}/cn-gmted-srtm-merge-102027-4000m-avg-1000m-cubicspline.tif ${env:CHINA-SOURCES}/cn-hydrographic-mask-merge-102027-1000m.tif
python $env:PATCHVRTPATH raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 1000 1000 raiseLandAIfNotInHydroMaskBAndScale.tif raiseLandAIfNotInHydroMaskBAndScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for raiseLandAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAAndScale.vrt ${env:CHINA-SOURCES}/cn-gmted-srtm-merge-102027-4000m-avg-1000m-cubicspline.tif
python $env:PATCHVRTPATH raiseLandAAndScale.vrt raiseLandAAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAAndScale.vrt raiseLandAAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 1000 1000 raiseLandAAndScale.tif raiseLandAAndScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for deleteLandAIfInHydroMaskB (translucent DEM)
gdalbuildvrt -resolution highest -overwrite deleteLandAIfInHydroMaskB.vrt ./raiseLandAIfNotInHydroMaskBAndScale.tif ${env:CHINA-SOURCES}/cn-hydrographic-mask-merge-102027-1000m.tif
python $env:PATCHVRTPATH deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 1000 1000 deleteLandAIfInHydroMaskB.tif deleteLandAIfInHydroMaskB_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for keepLandAIfNotInHydroMaskB (single print DEM)
gdalbuildvrt -resolution highest -overwrite keepLandAIfNotInHydroMaskB.vrt ${env:CHINA-SOURCES}/cn-gmted-srtm-merge-102027-4000m-avg-1000m-cubicspline.tif ${env:CHINA-SOURCES}/cn-hydrographic-mask-merge-102027-1000m.tif
python $env:PATCHVRTPATH keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 1000 1000 keepLandAIfNotInHydroMaskB.tif keepLandAIfNotInHydroMaskB_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#gdal
python ./generate-batch.py .\templates\cn-asia-conformal-conic-linear\cn-asia-conformal-conic-linear.json -gc

#run generated gdal commands

#tt
python ./generate-batch.py .\templates\cn-asia-conformal-conic-linear\cn-asia-conformal-conic-linear.json -gt

#run generate tt config first
python .\generate-batch.py .\templates\ak-na-conformal-conic-linear\ak-na-conformal-conic-linear.json -gt
#run from top dir
python ./TouchTerrain_standalone.py ./template-workspace/cn-asia-conformal-conic-linear/1000//touch_terrain_configs/CN.json
python ./TouchTerrain_standalone.py ./template-workspace/cn-asia-conformal-conic-linear/1000//touch_terrain_configs/CN-no-rivers.json
python ./TouchTerrain_standalone.py ./template-workspace/cn-asia-conformal-conic-linear/1000//touch_terrain_configs/CN-thru-river-cutout-base.json
python ./TouchTerrain_standalone.py ./template-workspace/cn-asia-conformal-conic-linear/1000//touch_terrain_configs/CN-single-print.json