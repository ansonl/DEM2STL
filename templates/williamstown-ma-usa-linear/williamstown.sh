# burn in values 3.6mx3.6m resolutino
roads 1
river 2
waterbodies 2
border-410m to get edge 3

#run this script from within the directory TOPDIR/template-workspace/TEMPLATE/RES/

#PATH setup
$env:TOPDIR = '../../../'

$env:PYTHONPATH = "$env:TOPDIR/templates/williamstown-ma-usa-linear/"
$env:PATCHVRTPATH = "$env:TOPDIR/workflow/patchVRT.py"

$env:SOURCES = "$env:TOPDIR/sources/"
$env:HYDROGRAPHICMASKS = "./"
${env:MAP-SOURCES} = "$env:TOPDIR/../maps/williamstown/"

#merge
gdalbuildvrt -resolution highest -overwrite ${env:MAP-SOURCES}/williamstown-area.vrt ${env:MAP-SOURCES}/williamstown-area.tif
#reproject
gdalwarp -overwrite -t_srs EPSG:32618 -r average  -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE" ${env:MAP-SOURCES}/williamstown-area.vrt ${env:MAP-SOURCES}/williamstown-area_utm18n.tif
#downscale
gdalwarp -overwrite -t_srs EPSG:32618 -tr 20.0 20.0 -r average -multi -of GTiff -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=FALSE" ${env:MAP-SOURCES}/williamstown-area_utm18n.tif ${env:MAP-SOURCES}/williamstown-area_utm18n_20m_avg.tif
#upscale
gdalwarp -overwrite -t_srs EPSG:32618 -tr 7.2 7.2 -r cubicspline -multi -of GTiff -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=FALSE" ${env:MAP-SOURCES}/williamstown-area_utm18n_20m_avg.tif ${env:MAP-SOURCES}/williamstown-area_utm18n_20m_avg_7-2_cubicspline.tif


#dem preprocessed from wgs84 21m to umt18n 3.6m with cubicspline in qgis
#clipped to boundary with border

# raiseLandAIfNotInHydroMaskBAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAIfNotInHydroMaskBAndScale.vrt ${env:MAP-SOURCES}/williamstown-area_utm18n_20m_avg_7-2_cubicspline.tif ${env:MAP-SOURCES}/williamstown-highway-river-border-merged.tif
python $env:PATCHVRTPATH raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 7.2 7.2 raiseLandAIfNotInHydroMaskBAndScale.tif raiseLandAIfNotInHydroMaskBAndScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for raiseLandAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAAndScale.vrt ${env:MAP-SOURCES}/williamstown-area_utm18n_20m_avg_7-2_cubicspline.tif ${env:MAP-SOURCES}/williamstown-highway-river-border-merged.tif
python $env:PATCHVRTPATH raiseLandAAndScale.vrt raiseLandAAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAAndScale.vrt raiseLandAAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 7.2 7.2 raiseLandAAndScale.tif raiseLandAAndScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#crop tifs to williamstown border + 400m buffer since region has only one border file
mkdir raiseLandAIfNotInHydroMaskBAndScale_tap
mkdir raiseLandAAndScale_tap

gdalwarp -overwrite -t_srs EPSG:32618 -of GTiff -tr 7.2 7.2 -cutline ${env:MAP-SOURCES}/williamstown-boundary-400m-buffer-filled.gpkg -crop_to_cutline ./raiseLandAIfNotInHydroMaskBAndScale_tap.tif ./raiseLandAIfNotInHydroMaskBAndScale_tap/williamstown.tif -r near -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"
gdalwarp -overwrite -t_srs EPSG:32618 -of GTiff -tr 7.2 7.2 -cutline ${env:MAP-SOURCES}/williamstown-boundary-400m-buffer-filled.gpkg -crop_to_cutline ./raiseLandAAndScale_tap.tif ./raiseLandAAndScale_tap/williamstown.tif -r near -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#run generate tt config first
python .\generate-batch.py .\templates\williamstown-ma-usa-linear\williamstown-ma-usa-linear.json -gt
#run from top dir
python ./TouchTerrain_standalone.py ./template-workspace/williamstown-ma-usa-linear/3.6/touch_terrain_configs/williamstown.json
python ./TouchTerrain_standalone.py ./template-workspace/williamstown-ma-usa-linear/3.6/touch_terrain_configs/williamstown-no-rivers.json