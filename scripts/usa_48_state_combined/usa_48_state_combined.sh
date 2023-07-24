#crop at 750 resolution to keep rivers but rivers will be at 0.08mm print res

gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 2500 2500 -cutline ./sources/USCB/tl_2022_us_state/usa_48_state_combined/usa_48_state_combined.gpkg -crop_to_cutline ./dem-feature-generation/raiseLandAIfNotInHydroMaskBAndScaleAt4m-250m-raised-460m.tif C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/raiseLandAIfNotInHydroMaskBAndScaleAt4m-250m-clipped/usa_48.tif -r cubicspline -multi -dstnodata -9999
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 2500 2500 -cutline ./sources/USCB/tl_2022_us_state/usa_48_state_combined/usa_48_state_combined.gpkg -crop_to_cutline ./dem-feature-generation/raiseLandAScaleAt4m-250m-raised-400m.tif C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/raiseLandAScaleAt4m-250m-clipped/usa_48.tif -r cubicspline -multi
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 2500 2500 -cutline ./sources/USCB/tl_2022_us_state/usa_48_state_combined/usa_48_state_combined.gpkg -crop_to_cutline ./dem-feature-generation/deleteLandAIfInHydroMaskB-250m-raised-460m.tif C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/deleteLandAIfInHydroMaskB-250m-clipped/usa_48.tif -r cubicspline -multi
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 2500 2500 -cutline ./sources/USCB/tl_2022_us_state/usa_48_state_combined/usa_48_state_combined.gpkg -crop_to_cutline ./dem-feature-generation/keepLandAIfNotInHydroMaskB-250m.tif C:/Users/ansonl/development/dem-to-stl-workflow/dem-feature-generation/keepLandAIfNotInHydroMaskB-250m-clipped/usa_48.tif -r cubicspline -multi

python ./TouchTerrain_standalone.py ./touch_terrain_configs_250m/usa_48.json
python ./TouchTerrain_standalone.py ./touch_terrain_configs_250m/usa_48-no-rivers.json
python ./TouchTerrain_standalone.py ./touch_terrain_configs_250m/usa_48-thru-river-cutout-base.json
python ./TouchTerrain_standalone.py ./touch_terrain_configs_250m/usa_48-single-print.json

echo 202 Mesh boolean subtracting usa_48
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/usa_48-no-rivers/usa_48_tile_1_1.STL ./state_stls_250m/usa_48/usa_48_tile_1_1.STL minus ./state_stls_250m/usa_48/usa_48_rivers.STL
echo usa_48 result $?
echo 203 Mesh boolean subtracting usa_48
time ./tools/gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls_250m/usa_48-no-rivers/usa_48_tile_1_1.STL ./state_stls_250m/usa_48-thru-river-cutout-base/usa_48_tile_1_1.STL minus ./state_stls_250m/usa_48-thru-river-cutout-base/usa_48_thru_rivers.STL
echo usa_48 result $?
