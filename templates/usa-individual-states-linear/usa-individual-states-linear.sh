#run this script from within the directory TOPDIR/template-workspace/TEMPLATE/RES/

#PATH setup
$env:TOPDIR = '../../../'

$env:PYTHONPATH = "$env:TOPDIR/templates/usa-individual-states-linear/"
$env:PATCHVRTPATH = "$env:TOPDIR/workflow/patchVRT.py"

$env:SOURCES = "$env:TOPDIR/sources/"
$env:HYDROGRAPHICMASKS = "$env:TOPDIR/hydrographic-masks/"

#create coastline only mask
#run in hydrographic mask folder
gdalwarp -overwrite -t_srs ESRI:102004 coastline_hydrographic_mask_merge_int16.vrt coastline_hydrographic_mask_merge_int16_102004.vrt -r near -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdalwarp -overwrite -tr 250.0 250.0 coastline_hydrographic_mask_merge_int16_102004.vrt coastline_hydrographic_mask_merge_int16_102004_250m.vrt -r max -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" coastline_hydrographic_mask_merge_int16_102004_250m.vrt coastline_hydrographic_mask_merge_int16_102004_250m.tif

#create VRT for raiseLandAIfNotInHydroMaskBAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAIfNotInHydroMaskBAndScale.vrt $env:SOURCES/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif $env:HYDROGRAPHICMASKS/north_america_hydrographic_mask_merge_102004_250m.tif
python $env:PATCHVRTPATH raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScale.vrt raiseLandAIfNotInHydroMaskBAndScale-250m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for raiseLandAndScale
gdalbuildvrt -resolution highest -overwrite raiseLandAAndScale.vrt $env:SOURCES/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif
python $env:PATCHVRTPATH raiseLandAAndScale.vrt raiseLandAAndScale
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAAndScale.vrt raiseLandAAndScale-250m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for deleteLandAIfInHydroMaskB (translucent DEM)
gdalbuildvrt -resolution highest -overwrite deleteLandAIfInHydroMaskB.vrt ./raiseLandAIfNotInHydroMaskBAndScale-250m.tif $env:HYDROGRAPHICMASKS/north_america_hydrographic_mask_merge_102004_250m.tif
python $env:PATCHVRTPATH deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB-250m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for keepLandAIfNotInHydroMaskB (single print DEM)
gdalbuildvrt -resolution highest -overwrite keepLandAIfNotInHydroMaskB.vrt $env:SOURCES/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif $env:HYDROGRAPHICMASKS/north_america_hydrographic_mask_merge_102004_250m.tif $env:HYDROGRAPHICMASKS/coastline_hydrographic_mask_merge_int16_102004_250m.tif
python $env:PATCHVRTPATH keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB-250m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#gdal

#tt