#downscale base land dem to 500x500m resolution
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap ./dems/7-5-arc-second-merged-reproject-102004.tif ./dems/7-5-arc-second-merged-500m-width-reproject-102004.tif -r cubicspline -multi -dstnodata -9999

#crop base land dem by hydro1k/hydrolakes merged dem (cutline is the smaller one)
#or export in QGIS, set export extent using hydro dem
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -te -8906000 -3328000 4305500 7828000 -te_srs ESRI:102004 ./dems/7-5-arc-second-merged-500m-width-reproject-102004.tif ./dems/7-5-arc-second-merged-500m-width-reproject-102004-extent-matched.tif -r cubicspline -multi -dstnodata -9999

#create version of land dem with locations that are <=0 (but covered by hydro) raised to 1 elevation
python gdal_calc.py -A ./dems/7-5-arc-second-merged-500m-width-reproject-102004-extent-matched.tif -B ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm.tif --outfile ./dems/7-5-arc-second-500m-width-hydro-raised-above-sea-level-102004.tif --calc="(A > 0) * A + logical_and(A <= 0, B > 0) * 1 + logical_and(A <= 0, B <= 0) * A" --overwrite

#raise nonhydro locations of 500x500 land dem
python gdal_calc.py -A ./dems/7-5-arc-second-merged-500m-width-reproject-102004-extent-matched.tif -B ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm.tif --outfile ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-raised-460.tif --calc="logical_and(B == 0, A > 4) * (A+460) + (B > 0) * A + logical_and(B == 0, A <= 0) * A + logical_and(B == 0, logical_and(A > 0, A <= 4)) * (A + A * 115)"

#raise nonhydro locations of 500x500 hydro fixed (raised) land dem
python gdal_calc.py -A ./dems/7-5-arc-second-500m-width-hydro-raised-above-sea-level-102004.tif -B ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm.tif --outfile ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-hydro-patched-raised-400.tif --calc="(A > 4) * (A+400) + (A<=0) * A + logical_and(A > 0, A<= 4) * (A + A * ((B > 0) * (14) + 100))"



gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/DE.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-raised-850.tif ./dems/7-5-arc-second-clipped-500m/DE.tif -r cubicspline -multi -dstnodata -9999

gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/DE.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-hydro-fixed-raised-800.tif ./dems/7-5-arc-second-clipped-500m-hydro-raised/DE-hydro-raised.tif -r cubicspline -multi -dstnodata -9999

gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/MD.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-raised-850.tif ./dems/7-5-arc-second-clipped-500m/MD.tif -r cubicspline -multi -dstnodata -9999

gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/MD.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-hydro-fixed-raised-800.tif ./dems/7-5-arc-second-clipped-500m-hydro-raised/MD-hydro-raised.tif -r cubicspline -multi -dstnodata -9999

#old method
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/SC.gpkg -crop_to_cutline ./dems/7-5-arc-second-merged.tif ./dems/7-5-arc-second-clipped-500m/SC.tif -r cubicspline -multi -dstnodata -9999
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/SC.gpkg -crop_to_cutline ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_merged_100m_ge_10sqkm.tif C:/Users/ansonl/development/dem-to-stl-workflow/dems/stream-lake-mask-clipped-500m/SC.tif -r cubicspline -multi


gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/SC.gpkg -crop_to_cutline ./dems/7-5-arc-second-clipped-500m/SC.tif ./dems/7-5-arc-second-clipped-500m/SC2.tif -r cubicspline -multi -dstnodata -9999