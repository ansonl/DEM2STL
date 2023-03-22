#create 200x200m resolution hydrolakes
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 200.0 200.0 -tap ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_merged_100m_ge_10sqkm.tif C:/Users/ansonl/development/dem-to-stl-workflow/usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_200m_ge_10sqkm.tif -r cubicspline -multi

#downscale base land dem to 200x200m resolution
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 200.0 200.0 -tap ./dems/7-5-arc-second-merged-reproject-102004.tif ./dems/7-5-arc-second-merged-200m-width-reproject-102004.tif -r cubicspline -multi -dstnodata -9999

#crop base land dem by hydro1k/hydrolakes merged dem (cutline is the smaller one)
#or export in QGIS, set export extent using hydro dem
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 200.0 200.0 -te -8906000 -3328000 4305400 7828000 -te_srs ESRI:102004 ./dems/7-5-arc-second-merged-200m-width-reproject-102004.tif ./dems/7-5-arc-second-merged-200m-width-reproject-102004-extent-matched.tif -r cubicspline -multi -dstnodata -9999

#create version of land dem with locations that are <=0 (but covered by hydro) raised to 1 elevation
python gdal_calc.py -A ./dems/7-5-arc-second-merged-200m-width-reproject-102004-extent-matched.tif -B ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_200m_ge_10sqkm.tif --outfile ./dems/7-5-arc-second-200m-width-hydro-raised-above-sea-level-102004.tif --calc="(A > 0) * A + logical_and(A <= 0, B > 0) * 1 + logical_and(A <= 0, B <= 0) * A" --overwrite

#raise nonhydro locations of 200x200 land dem. 
# Raise locations with no hydro and (>4m by 160m)/(>0, <=4 by scaled version to 160m at 4m). 
# Keep locations under hydro and 0m unchanged. 
# Accentuate coastlines and areas under 4m. Deepen stream paths vs surroundings slightly not super deep since this isn't for glow material rivers. This also emphasizes below sea level areas. Displayed river width is due to 200mx200m resolution hydro DEM and diagonals and turns end up as 1000mx1000m. 
python gdal_calc.py -A ./dems/7-5-arc-second-merged-200m-width-reproject-102004-extent-matched.tif -B ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_200m_ge_10sqkm.tif --outfile ./dems/dems-ready-to-cut/7-5-arc-second-merged-200m-width-raised-160.tif --calc="logical_and(B == 0, A > 4) * (A+160) + (B > 0) * A + logical_and(B == 0, A <= 0) * A + logical_and(B == 0, logical_and(A > 0, A <= 4)) * (A + A * 40)"

#raise nonhydro locations of 200x200 hydro fixed (raised) land dem. 
# Raise locations >4m by 100m (100m ensures that this area will be just below the previous DEM that has areas surrounding water artificially raised by 160m). This DEM should not poke above the previous DEM unless we display water there (because the previous DEM did not raise the water areas).
# Raise location >0,<=4m AND has water over it, <=4m by scaled amount to (39) at 4m. These areas will poke above the previous DEM in areas with water since we did not raise them in previous DEM. If no water there, leave unchanged so we don't poke above previous DEM in low areas with no hydro.
python gdal_calc.py -A ./dems/7-5-arc-second-200m-width-hydro-raised-above-sea-level-102004.tif -B ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_200m_ge_10sqkm.tif --outfile ./dems/dems-ready-to-cut/7-5-arc-second-merged-200m-width-hydro-patched-raised-100.tif --calc="(A > 4) * (A+100) + (A<=0) * A + logical_and(A > 0, A<= 4) * (A + A * ((B > 0) * 39))"