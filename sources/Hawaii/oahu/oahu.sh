#crop to oahu
gdalwarp -overwrite -t_srs EPSG:32604 -of GTiff -tr 50 50 -cutline ./oahu.gpkg -crop_to_cutline ../hawaii_gmted2010_strm_merge_32604_200m_50m_cubicspline.tif oahu_32604_200m_50m_cubicspline.tif -r near -multi -dstnodata -9999

$env:PYTHONPATH = './'

#create VRT for raiseLandAIfNotInHydroMaskBAndScaleAt4m
gdalbuildvrt -resolution lowest -overwrite raiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt oahu_32604_200m_50m_cubicspline.tif oahu_500m_inland_coastline_dissolved_clipped_1500m_50m.tif
python ../../../workflow/patchVRT.py raiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt raiseLandAIfNotInHydroMaskBAndScaleAt4m
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt raiseLandAIfNotInHydroMaskBAndScaleAt4m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for raiseLandAScaleAt4m
#gdalbuildvrt -resolution highest -overwrite raiseLandAScaleAt4m.vrt raiseOverSeaLevelLandAIfInHydroMaskB.vrt ./coastline_mask_32604_250m.tif
gdalbuildvrt -resolution lowest -overwrite raiseLandAScaleAt4m.vrt ./oahu_32604_200m_50m_cubicspline.tif oahu_500m_inland_coastline_dissolved_clipped_1500m_50m.tif
python ../../../workflow/patchVRT.py raiseLandAScaleAt4m.vrt raiseLandAScaleAt4m
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAScaleAt4m.vrt raiseLandAScaleAt4m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for deleteLandAIfInHydroMaskB (translucent DEM)
gdalbuildvrt -resolution lowest -overwrite deleteLandAIfInHydroMaskB.vrt ./raiseLandAIfNotInHydroMaskBAndScaleAt4m.tif ./oahu_500m_inland_coastline_dissolved_clipped_1500m_50m.tif
python ../../../workflow/patchVRT.py deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB.tif --config GDAL_VRT_ENABLE_PYTHON YES

#use source tif for single print

#set up dem feature generation
mkdir ./dem-feature-generation/raiseLandAIfNotInHydroMaskBAndScaleAt4m-20m-clipped/
mkdir ./dem-feature-generation/raiseLandAScaleAt4m-20m-clipped/
mkdir ./dem-feature-generation/deleteLandAIfInHydroMaskB-20m-clipped/
mkdir ./touch_terrain_configs_20m/
mkdir ./state_stls_20m/
mkdir ./tmp/state_stls_20m/


mv raiseLandAIfNotInHydroMaskBAndScaleAt4m.tif ./dem-feature-generation/raiseLandAIfNotInHydroMaskBAndScaleAt4m-20m-clipped/oahu.tif
mv raiseLandAScaleAt4m.tif ./dem-feature-generation/raiseLandAScaleAt4m-20m-clipped/oahu.tif
mv deleteLandAIfInHydroMaskB.tif ./dem-feature-generation/deleteLandAIfInHydroMaskB-20m-clipped/oahu.tif

python ..\..\..\generate-touch-terrain-config.py oahu

python ../../../TouchTerrain_standalone.py ./touch_terrain_configs_20m/oahu.json
python ../../../TouchTerrain_standalone.py ./touch_terrain_configs_20m/oahu-no-rivers.json
python ../../../TouchTerrain_standalone.py ./touch_terrain_configs_20m/oahu-thru-river-cutout-base.json
python ../../../TouchTerrain_standalone.py ./touch_terrain_configs_20m/oahu-single-print.json #"importedDEM": "./dem-feature-generation/raiseLandAIfNotInHydroMaskBAndScaleAt4m-20m-clipped/oahu.tif",
# "ignore_leq": 0,
# "min_elev": 0,



../../../tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_20m/oahu-no-rivers/oahu_tile_1_1.STL ./state_stls_20m/oahu/oahu_tile_1_1.STL minus ./state_stls_20m/oahu/oahu_rivers.STL
../../../tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_20m/oahu-no-rivers/oahu_tile_1_1.STL ./state_stls_20m/oahu-thru-river-cutout-base/oahu_tile_1_1.STL minus ./state_stls_20m/oahu-thru-river-cutout-base/oahu_thru_rivers.STL

#lowpoly
../../../tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_20m/oahu-no-rivers/oahu_tile_low_poly_001.STL ./state_stls_20m/oahu/oahu_tile_low_poly_001.STL minus ./state_stls_20m/oahu/oahu_rivers_low_poly_001.STL
../../../tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_20m/oahu-no-rivers/oahu_tile_low_poly_001.STL ./state_stls_20m/oahu/oahu_tile_low_poly_005.STL minus ./state_stls_20m/oahu/oahu_rivers_low_poly_005.STL