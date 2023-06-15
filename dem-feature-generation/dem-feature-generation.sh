#$env:GDAL_VRT_ENABLE_PYTHON = 'YES'
$env:PYTHONPATH = './'

#create VRT for raiseOverSeaLevelLandAIfInHydroMaskB
#need to manually add subclass and PixelFunction
#gdalbuildvrt -resolution highest -overwrite raiseOverSeaLevelLandAIfInHydroMaskB.vrt ../sources/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif

#create VRT for raiseLandAIfNotInHydroMaskBAndScaleAt4m
gdalbuildvrt -resolution highest -overwrite raiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt ../sources/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt raiseLandAIfNotInHydroMaskBAndScaleAt4m-250m-raised-460m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for raiseLandAScaleAt4m
gdalbuildvrt -resolution highest -overwrite raiseLandAScaleAt4m.vrt raiseOverSeaLevelLandAIfInHydroMaskB.vrt ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdalbuildvrt -resolution highest -overwrite raiseLandAScaleAt4m.vrt ../sources/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAScaleAt4m.vrt raiseLandAScaleAt4m-250m-raised-400m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for deleteLandAIfInHydroMaskB (translucent DEM)
gdalbuildvrt -resolution highest -overwrite deleteLandAIfInHydroMaskB.vrt ./raiseLandAIfNotInHydroMaskBAndScaleAt4m-250m-raised-460m.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB-250m-raised-460m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for keepLandAIfNotInHydroMaskB (single print DEM)
gdalbuildvrt -resolution highest -overwrite keepLandAIfNotInHydroMaskB.vrt ../sources/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB-250m.tif --config GDAL_VRT_ENABLE_PYTHON YES