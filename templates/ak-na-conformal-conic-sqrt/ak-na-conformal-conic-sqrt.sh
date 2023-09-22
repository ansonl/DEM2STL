#run this script from within the directory TOPDIR/template-workspace/TEMPLATE/RES/

#PATH setup
$env:TOPDIR = '../../../'

$env:PYTHONPATH = "$env:TOPDIR/templates/ak-na-conformal-conic-sqrt/"
$env:PATCHVRTPATH = "$env:TOPDIR/workflow/patchVRT.py"

#use AK linear template  rasters
$env:AKDEMPATH = "$env:TOPDIR/template-workspace/ak-na-conformal-conic-linear/250/ak_gmted2010_srtm_merge_102009_1000m_avg_250m_cubicspline.tif"
$env:AKHYDROMASKMERGEDPATH = "$env:TOPDIR/template-workspace/ak-na-conformal-conic-linear/250/ak_hydrographic_mask_merge_102009_250m.tif"
$env:AKCOASTLINEONLYMASKPATH = "$env:TOPDIR/template-workspace/ak-na-conformal-conic-linear/250/ak_coastline_hydrographic_mask_merge_int16_102009_250m.tif"

$env:SOURCES = "$env:TOPDIR/sources/"
$env:HYDROGRAPHICMASKS = "$env:TOPDIR/hydrographic-masks/"

#create VRT for globalScaleLandA
gdalbuildvrt -resolution highest -overwrite globalScaleLandA.vrt $env:AKDEMPATH
python $env:PATCHVRTPATH globalScaleLandA.vrt globalScaleLandA
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" globalScaleLandA.vrt globalScaleLandA.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for raiseLandAIfNotInHydroMaskBAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAIfNotInHydroMaskBAndScale.vrt globalScaleLandA.tif $env:AKHYDROMASKMERGEDPATH
python $env:PATCHVRTPATH raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 250 250 raiseLandAIfNotInHydroMaskBAndScale.tif raiseLandAIfNotInHydroMaskBAndScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for raiseLandAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAAndScale.vrt globalScaleLandA.tif
python $env:PATCHVRTPATH raiseLandAAndScale.vrt raiseLandAAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAAndScale.vrt raiseLandAAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 250 250 raiseLandAAndScale.tif raiseLandAAndScale_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for deleteLandAIfInHydroMaskB (translucent DEM)
gdalbuildvrt -resolution highest -overwrite deleteLandAIfInHydroMaskB.vrt ./raiseLandAIfNotInHydroMaskBAndScale.tif $env:AKHYDROMASKMERGEDPATH
python $env:PATCHVRTPATH deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 250 250 deleteLandAIfInHydroMaskB.tif deleteLandAIfInHydroMaskB_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create VRT for keepLandAIfNotInHydroMaskB (single print DEM)
gdalbuildvrt -resolution highest -overwrite keepLandAIfNotInHydroMaskB.vrt globalScaleLandA.tif $env:AKHYDROMASKMERGEDPATH $env:AKCOASTLINEONLYMASKPATH
python $env:PATCHVRTPATH keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdalwarp -overwrite -tr 250 250 keepLandAIfNotInHydroMaskB.tif keepLandAIfNotInHydroMaskB_tap.tif -r near -tap -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#crop tifs to AK border since AK has only one border file
mkdir raiseLandAIfNotInHydroMaskBAndScale_tap
mkdir raiseLandAAndScale_tap
mkdir deleteLandAIfInHydroMaskB_tap
mkdir keepLandAIfNotInHydroMaskB_tap
gdalwarp -overwrite -t_srs ESRI:102009 -of GTiff -tr 250 250 -cutline $env:SOURCES/USCB/tl_2022_us_state/split_individual/AK.gpkg -crop_to_cutline ./raiseLandAIfNotInHydroMaskBAndScale_tap.tif ./raiseLandAIfNotInHydroMaskBAndScale_tap/AK.tif -r near -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"
gdalwarp -overwrite -t_srs ESRI:102009 -of GTiff -tr 250 250 -cutline $env:SOURCES/USCB/tl_2022_us_state/split_individual/AK.gpkg -crop_to_cutline ./raiseLandAAndScale_tap.tif ./raiseLandAAndScale_tap/AK.tif -r near -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"
gdalwarp -overwrite -t_srs ESRI:102009 -of GTiff -tr 250 250 -cutline $env:SOURCES/USCB/tl_2022_us_state/split_individual/AK.gpkg -crop_to_cutline ./deleteLandAIfInHydroMaskB_tap.tif ./deleteLandAIfInHydroMaskB_tap/AK.tif -r near -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"
gdalwarp -overwrite -t_srs ESRI:102009 -of GTiff -tr 250 250 -cutline $env:SOURCES/USCB/tl_2022_us_state/split_individual/AK.gpkg -crop_to_cutline ./keepLandAIfNotInHydroMaskB_tap.tif ./keepLandAIfNotInHydroMaskB_tap/AK.tif -r near -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#run generate tt config first
cd ../../../
python .\generate-batch.py .\templates\ak-na-conformal-conic-sqrt\ak-na-conformal-conic-sqrt.json -gt
#run from top dir
python ./TouchTerrain_standalone.py ./template-workspace/ak-na-conformal-conic-sqrt/250/touch_terrain_configs/AK.json
python ./TouchTerrain_standalone.py ./template-workspace/ak-na-conformal-conic-sqrt/250/touch_terrain_configs/AK-no-rivers.json
python ./TouchTerrain_standalone.py ./template-workspace/ak-na-conformal-conic-sqrt/250/touch_terrain_configs/AK-thru-river-cutout-base.json
python ./TouchTerrain_standalone.py ./template-workspace/ak-na-conformal-conic-sqrt/250/touch_terrain_configs/AK-single-print.json
