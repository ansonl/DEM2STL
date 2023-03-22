gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/CT.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-raised-460.tif ./dems/7-5-arc-second-clipped-500m/CT.tif -r cubicspline -multi -dstnodata -9999
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/CT.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-hydro-patched-raised-400.tif C:/Users/ansonl/development/dem-to-stl-workflow/dems/7-5-arc-second-clipped-500m-hydro-patched/CT-hydro-patched.tif -r cubicspline -multi
python ./TouchTerrain_standalone.py ./touch_terrain_configs/CT.json
python ./TouchTerrain_standalone.py ./touch_terrain_configs/CT-no-rivers.json

./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/CT-no-rivers/CT-hydro-patched_tile_1_1.STL ./state_stls/CT/CT_tile_1_1.STL minus ./state_stls/CT/CT_rivers.STL

./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/CT-no-rivers/CT-hydro-patched_tile_blender.STL ./state_stls/CT/CT_tile_blender.STL minus ./state_stls/CT/CT_rivers.STL