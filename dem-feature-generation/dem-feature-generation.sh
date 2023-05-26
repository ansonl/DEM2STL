# reproject land dem to 102004
gdalwarp -overwrite -t_srs ESRI:102004 ../sources/north_america_gmted2010_srtm_merge.tif north_america_gmted2010_srtm_merge_102004_bilinear.vrt -r bilinear -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_gmted2010_srtm_merge_102004.vrt north_america_gmted2010_srtm_merge_102004.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_gmted2010_srtm_merge_102004_bilinear.vrt north_america_gmted2010_srtm_merge_102004_bilinear.tif

#test reproject and downscale in one op
gdalwarp -overwrite -t_srs ESRI:102004 -tr 500 500 -tap -r average  -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE" ../sources/north_america_gmted2010_srtm_merge.tif north_america_gmted2010_srtm_merge_102004_500m_direct.tif

gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_gmted2010_srtm_merge_102004_bilinear.vrt north_america_gmted2010_srtm_merge_102004_bilinear.tif

#cubic test
gdalwarp -overwrite -t_srs ESRI:102004 ../sources/north_america_gmted2010_srtm_merge.tif north_america_gmted2010_srtm_merge_102004_cubic.vrt -r cubic -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_gmted2010_srtm_merge_102004_cubic.vrt north_america_gmted2010_srtm_merge_102004_cubic.tif


#downscale land dem to 500x500m
gdalwarp -overwrite -t_srs ESRI:102004 -tr 500.0 500.0 -tap north_america_gmted2010_srtm_merge_102004_bilinear.tif north_america_gmted2010_srtm_merge_102004_500m_tap.vrt -r average -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_gmted2010_srtm_merge_102004_500m_tap.vrt north_america_gmted2010_srtm_merge_102004_500m_tap.tif

#upscale land dem to 250x250m
gdalwarp -overwrite -tr 250.0 250.0 north_america_gmted2010_srtm_merge_102004_500m.tif north_america_gmted2010_srtm_merge_102004_250m.vrt -r cubicspline -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_gmted2010_srtm_merge_102004_250m.vrt north_america_gmted2010_srtm_merge_102004_250m.tif


$env:GDAL_VRT_ENABLE_PYTHON = 'YES'
$env:PYTHONPATH = './'

#ME test
gdalbuildvrt -resolution highest -overwrite MEraiseOverSeaLevelLandAIfInHydroMaskB.vrt source-dem-250m-clipped/ME.tif hydrographic-mask-250m-clipped/ME.tif
gdalbuildvrt -resolution highest -overwrite MEraiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt source-dem-250m-clipped/ME.tif hydrographic-mask-250m-clipped/ME.tif
gdalbuildvrt -resolution highest -overwrite MEraiseLandAScaleAt4m.vrt MEraiseOverSeaLevelLandAIfInHydroMaskB.vrt hydrographic-mask-250m-clipped/ME.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" MEraiseOverSeaLevelLandAIfInHydroMaskB.vrt MEraiseOverSeaLevelLandAIfInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" MEraiseLandAScaleAt4m.vrt MEraiseLandAScaleAt4m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for raiseOverSeaLevelLandAIfInHydroMaskB
#need to manually add subclass and PixelFunction
gdalbuildvrt -resolution highest -overwrite raiseOverSeaLevelLandAIfInHydroMaskB.vrt ../sources/north_america_gmted2010_srtm_merge_102004_500m_avg_250m_cubicspline.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif

#create VRT for raiseLandAIfNotInHydroMaskBAndScaleAt4m
gdalbuildvrt -resolution highest -overwrite raiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt ../sources/north_america_gmted2010_srtm_merge_102004_500m_avg_250m_cubicspline.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt raiseLandAIfNotInHydroMaskBAndScaleAt4m-250m-raised-460m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for raiseLandAScaleAt4m
gdalbuildvrt -resolution highest -overwrite raiseLandAScaleAt4m.vrt raiseOverSeaLevelLandAIfInHydroMaskB.vrt ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAScaleAt4m.vrt raiseLandAScaleAt4m-250m-raised-400m.tif --config GDAL_VRT_ENABLE_PYTHON YES