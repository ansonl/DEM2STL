#$env:GDAL_VRT_ENABLE_PYTHON = 'YES'
$env:PYTHONPATH = './'

#create VRT for raiseOverSeaLevelLandAIfInHydroMaskB
#need to manually add subclass and PixelFunction
#gdalbuildvrt -resolution highest -overwrite raiseOverSeaLevelLandAIfInHydroMaskB.vrt ../sources/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif

#create VRT for raiseLandAIfNotInHydroMaskBAndScaleAt4m
gdalbuildvrt -resolution highest -overwrite raiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt ../sources/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt raiseLandAIfNotInHydroMaskBAndScaleAt4m-250m-raised-460m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for raiseLandAScaleAt4m
#gdalbuildvrt -resolution highest -overwrite raiseLandAScaleAt4m.vrt raiseOverSeaLevelLandAIfInHydroMaskB.vrt ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdalbuildvrt -resolution highest -overwrite raiseLandAScaleAt4m.vrt ../sources/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAScaleAt4m.vrt raiseLandAScaleAt4m-250m-raised-400m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for deleteLandAIfInHydroMaskB (translucent DEM)
gdalbuildvrt -resolution highest -overwrite deleteLandAIfInHydroMaskB.vrt ./raiseLandAIfNotInHydroMaskBAndScaleAt4m-250m-raised-460m.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB-250m-raised-460m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for keepLandAIfNotInHydroMaskB (single print DEM)
gdalbuildvrt -resolution highest -overwrite keepLandAIfNotInHydroMaskB.vrt ../sources/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif ../hydrographic-masks/north_america_hydrographic_mask_merge_102004_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB-250m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#log scale test
gdalbuildvrt -resolution highest -overwrite CTglobalLogScaleLandA.vrt ../sources/CT_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif ../hydrographic-masks/CT_hydrographic_mask_merge_102004_250m.tif
gdalbuildvrt -resolution highest -overwrite CTglobalLogScaleLandADeleteIfInHydroMaskB.vrt ../sources/CT_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif ../hydrographic-masks/CT_hydrographic_mask_merge_102004_250m.tif
gdal_translate -ot Float32 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" VAglobalLogScaleLandA.vrt CTglobalLogScaleLandA-250m.tif --config GDAL_VRT_ENABLE_PYTHON YES
gdal_translate -ot Float32 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" VAglobalLogScaleLandADeleteIfInHydroMaskB.vrt CTglobalLogScaleLandADeleteIfInHydroMaskB-250m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#log CT test
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 250 250 -cutline ./sources/USCB/tl_2022_us_state/split_individual/CT.gpkg -crop_to_cutline ./dem-feature-generation/CTglobalLogScaleLandA-250m.tif C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/globalLogScaleLandA-250m-clipped/CT.tif -r near -multi -dstnodata -9999
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 250 250 -cutline ./sources/USCB/tl_2022_us_state/split_individual/CT.gpkg -crop_to_cutline ./dem-feature-generation/CTglobalLogScaleLandADeleteIfInHydroMaskB-250m.tif C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/globalLogScaleLandADeleteIfInHydroMaskB-250m-clipped/CT.tif -r near -multi
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 250 250 -cutline ./sources/USCB/tl_2022_us_state/split_individual/VA.gpkg -crop_to_cutline ./dem-feature-generation/CTglobalLogScaleLandA-250m.tif C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/globalLogScaleLandA-250m-clipped/VA.tif -r near -multi -dstnodata -9999
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 250 250 -cutline ./sources/USCB/tl_2022_us_state/split_individual/VA.gpkg -crop_to_cutline ./dem-feature-generation/CTglobalLogScaleLandADeleteIfInHydroMaskB-250m.tif C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/globalLogScaleLandADeleteIfInHydroMaskB-250m-clipped/VA.tif -r near -multi

gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 250 250 -cutline ./sources/USCB/tl_2022_us_state/split_individual/CT.gpkg -crop_to_cutline ./dem-feature-generation/globalLogScaleLandA-250m.tif C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/globalLogScaleLandA-250m-clipped/CT.tif -r near -multi -dstnodata -9999
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 250 250 -cutline ./sources/USCB/tl_2022_us_state/split_individual/CT.gpkg -crop_to_cutline ./dem-feature-generation/globalLogScaleLandADeleteIfInHydroMaskB-250m.tif C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/globalLogScaleLandADeleteIfInHydroMaskB-250m-clipped/CT.tif -r near -multi

python ./TouchTerrain_standalone.py ./touch_terrain_configs_250m/CT-log-scale-no-rivers.json
python ./TouchTerrain_standalone.py ./touch_terrain_configs_250m/CT-log-scale-thru-river-cutout-base.json

python ./TouchTerrain_standalone.py ./touch_terrain_configs_250m/VA-log-scale-no-rivers.json
python ./TouchTerrain_standalone.py ./touch_terrain_configs_250m/VA-log-scale-thru-river-cutout-base.json