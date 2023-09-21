#run this script from within the directory TOPDIR/template-workspace/TEMPLATE/RES/

#PATH setup
$env:TOPDIR = '../../../'

$env:PYTHONPATH = "$env:TOPDIR/templates/ak-na-conformal-conic-linear/"
$env:PATCHVRTPATH = "$env:TOPDIR/workflow/patchVRT.py"

$env:SOURCES = "$env:TOPDIR/sources/"
$env:HYDROGRAPHICMASKS = "$env:TOPDIR/hydrographic-masks/"
q
#hydrographic mask preparation
#create AK coastline mask
gdalbuildvrt -resolution highest -overwrite ak_coastline_hydrographic_mask_merge.vrt $env:HYDROGRAPHICMASKS/coastline/ak-*.tif
gdal_translate -ot Int16 ak_coastline_hydrographic_mask_merge.vrt ak_coastline_hydrographic_mask_merge_int16.vrt
#merge coastline, hydro1k, hydrolakes masks
gdalbuildvrt -resolution highest -overwrite ak_hydrographic_mask_merge.vrt ak_coastline_hydrographic_mask_merge_int16.vrt ak-main-hydro1k.tif ak-main-hydrolakes.tif
#reproject to 102009 and downscale to 250x250m
gdalwarp -overwrite -t_srs ESRI:102009 -tr 250.0 250.0 ak_hydrographic_mask_merge.vrt ak_hydrographic_mask_merge_102009_250m.vrt -r max -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" ak_hydrographic_mask_merge_102009_250m.vrt ak_hydrographic_mask_merge_102009_250m.tif

#create coastline only mask
#run in workspace folder
gdalwarp -overwrite -t_srs ESRI:102009 ak_coastline_hydrographic_mask_merge_int16.vrt ak_coastline_hydrographic_mask_merge_int16_102009.vrt -r near -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdalwarp -overwrite -tr 250.0 250.0 ak_coastline_hydrographic_mask_merge_int16_102009.vrt ak_coastline_hydrographic_mask_merge_int16_102009_250m.vrt -r max -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" ak_coastline_hydrographic_mask_merge_int16_102009_250m.vrt ak_coastline_hydrographic_mask_merge_int16_102009_250m.tif

#crop srtm to AK
#merge AK main and far west
gdalbuildvrt -resolution highest -overwrite ak_gmted2010_srtm_merge.vrt ak_main_gmted2010_srtm_merge.tif ak-far-west-srtm.tif
#reproject ak_gmted2010_srtm_merge.tif to 102009 avg and downscale to 1000 in QGIS to avoid gaps. OUTPUT ak_gmted2010_srtm_merge_102009_1000m_average.tif
#250x250 upscale in cubicspline
gdalwarp -overwrite -t_srs ESRI:102009 -tr 250.0 250.0 -r cubicspline -multi -of GTiff -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=FALSE" ak_gmted2010_srtm_merge_102009_1000m_average.tif ak_gmted2010_srtm_merge_102009_1000m_avg_250m_cubicspline.tif
#DO UPSACLE

#create VRT for raiseLandAIfNotInHydroMaskBAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAIfNotInHydroMaskBAndScale.vrt ak_gmted2010_srtm_merge_102009_1000m_avg_250m_cubicspline.tif ak_hydrographic_mask_merge_102009_250m.tif
python $env:PATCHVRTPATH raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for raiseLandAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAAndScale.vrt ak_gmted2010_srtm_merge_102009_1000m_avg_250m_cubicspline.tif
python $env:PATCHVRTPATH raiseLandAAndScale.vrt raiseLandAAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAAndScale.vrt raiseLandAAndScale.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for deleteLandAIfInHydroMaskB (translucent DEM)
gdalbuildvrt -resolution highest -overwrite deleteLandAIfInHydroMaskB.vrt ./raiseLandAIfNotInHydroMaskBAndScale.tif ak_hydrographic_mask_merge_102009_250m.tif
python $env:PATCHVRTPATH deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for keepLandAIfNotInHydroMaskB (single print DEM)
gdalbuildvrt -resolution highest -overwrite keepLandAIfNotInHydroMaskB.vrt ak_gmted2010_srtm_merge_102009_1000m_avg_250m_cubicspline.tif ak_hydrographic_mask_merge_102009_250m.tif coastline_hydrographic_mask_merge_int16_102004_250m.tif
python $env:PATCHVRTPATH keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES

#crop tifs to AK border
mkdir raiseLandAIfNotInHydroMaskBAndScale
mkdir raiseLandAAndScale
mkdir deleteLandAIfInHydroMaskB
mkdir keepLandAIfNotInHydroMaskB
gdalwarp -overwrite -t_srs ESRI:102009 -of GTiff -tr 250 250 -cutline $env:SOURCES/USCB/tl_2022_us_state/split_individual/AK.gpkg -crop_to_cutline ./raiseLandAIfNotInHydroMaskBAndScale.tif ./raiseLandAIfNotInHydroMaskBAndScale/AK.tif -r near -multi -dstnodata -9999
gdalwarp -overwrite -t_srs ESRI:102009 -of GTiff -tr 250 250 -cutline $env:SOURCES/USCB/tl_2022_us_state/split_individual/AK.gpkg -crop_to_cutline ./raiseLandAAndScale.tif ./raiseLandAAndScale/AK.tif -r near -multi
gdalwarp -overwrite -t_srs ESRI:102009 -of GTiff -tr 250 250 -cutline $env:SOURCES/USCB/tl_2022_us_state/split_individual/AK.gpkg -crop_to_cutline ./deleteLandAIfInHydroMaskB.tif ./deleteLandAIfInHydroMaskB/AK.tif -r near -multi
gdalwarp -overwrite -t_srs ESRI:102009 -of GTiff -tr 250 250 -cutline $env:SOURCES/USCB/tl_2022_us_state/split_individual/AK.gpkg -crop_to_cutline ./keepLandAIfNotInHydroMaskB.tif ./keepLandAIfNotInHydroMaskB/AK.tif -r near -multi

#run generate tt config first
python 
#run from top dir
python ./TouchTerrain_standalone.py ./touch_terrain_configs/ak-na-conformal-conic/250/AK.json
python ./TouchTerrain_standalone.py ./touch_terrain_configs/ak-na-conformal-conic/250/AK-no-rivers.json
python ./TouchTerrain_standalone.py ./touch_terrain_configs/ak-na-conformal-conic/250/AK-thru-river-cutout-base.json
python ./TouchTerrain_standalone.py ./touch_terrain_configs/ak-na-conformal-conic/250/AK-single-print.json
