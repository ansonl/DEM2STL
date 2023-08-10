#downscale from 20x20m to 200x200m 
gdalwarp -overwrite -t_srs EPSG:32604 -tr 200.0 200.0 -r average -multi -of GTiff -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=FALSE" hawaii_gmted2010_strm_merge_32604.tif hawaii_gmted2010_strm_merge_32604_200m_average.tif

#upscale from 200x200m to 50x50m 
gdalwarp -overwrite -t_srs EPSG:32604 -tr 50.0 50.0 -r cubicspline -multi -of GTiff -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=FALSE" hawaii_gmted2010_strm_merge_32604_200m_average.tif hawaii_gmted2010_strm_merge_32604_200m_50m_cubicspline.tif

#crop hawaii_gmted2010_strm_merge_32604_200m_20m_cubicspline.tif to hawaii coastline


$env:PYTHONPATH = '../../dem-feature-generation/'

#create VRT for raiseLandAIfNotInHydroMaskBAndScaleAt4m
gdalbuildvrt -resolution highest -overwrite raiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt ./hawaii_gmted2010_strm_merge_32604_250m.tif ./coastline_mask_32604_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAIfNotInHydroMaskBAndScaleAt4m.vrt raiseLandAIfNotInHydroMaskBAndScaleAt4m-250m-raised-460m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for raiseLandAScaleAt4m
#gdalbuildvrt -resolution highest -overwrite raiseLandAScaleAt4m.vrt raiseOverSeaLevelLandAIfInHydroMaskB.vrt ./coastline_mask_32604_250m.tif
gdalbuildvrt -resolution highest -overwrite raiseLandAScaleAt4m.vrt ./hawaii_gmted2010_strm_merge_32604_250m.tif ./coastline_mask_32604_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" raiseLandAScaleAt4m.vrt raiseLandAScaleAt4m-250m-raised-400m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for deleteLandAIfInHydroMaskB (translucent DEM)
gdalbuildvrt -resolution highest -overwrite deleteLandAIfInHydroMaskB.vrt ./raiseLandAIfNotInHydroMaskBAndScaleAt4m-250m-raised-460m.tif ./coastline_mask_32604_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" deleteLandAIfInHydroMaskB.vrt deleteLandAIfInHydroMaskB-250m-raised-460m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#create VRT for keepLandAIfNotInHydroMaskB (single print DEM)
gdalbuildvrt -resolution highest -overwrite keepLandAIfNotInHydroMaskB.vrt ./hawaii_gmted2010_strm_merge_32604_250m.tif ./coastline_mask_32604_250m.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" keepLandAIfNotInHydroMaskB.vrt keepLandAIfNotInHydroMaskB-250m.tif --config GDAL_VRT_ENABLE_PYTHON YES

#build touch terrain configs and move to current folder + change source files
python ../../TouchTerrain_standalone.py ./HI.json
python ../../TouchTerrain_standalone.py ./HI-no-rivers.json
python ../../TouchTerrain_standalone.py ./HI-thru-river-cutout-base.json
python ../../TouchTerrain_standalone.py ./HI-single-print.json

#boolean
echo 6 Mesh boolean subtracting HI
time ../../tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/HI-no-rivers/raiseLandAScaleAt4m-250m-raised-400m_tile_1_1.STL ./state_stls_250m/HI/raiseLandAIfNotInHydroMaskBAndScaleAt4m-250m-raised-460m_tile_1_1.STL minus ./state_stls_250m/HI/HI_rivers.STL
echo HI result $?
echo 7 Mesh boolean subtracting HI
time ../../tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/HI-no-rivers/raiseLandAScaleAt4m-250m-raised-400m_tile_1_1.STL ./state_stls_250m/HI-thru-river-cutout-base/deleteLandAIfInHydroMaskB-250m-raised-460m_tile_1_1.STL minus ./state_stls_250m/HI-thru-river-cutout-base/HI_thru_rivers.STL
echo HI result $?