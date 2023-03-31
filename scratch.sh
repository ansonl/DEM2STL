#downscale base land dem to 500x500m resolution
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap ./dems/7-5-arc-second-merged-reproject-102004.tif ./dems/7-5-arc-second-merged-500m-width-reproject-102004.tif -r cubicspline -multi -co COMPRESS=ZSTD -co PREDICTOR=2 -wo "NUM_THREADS=6/ALL_CPUS" 

#crop base land dem by hydro1k/hydrolakes merged dem (cutline is the smaller one)
#or export in QGIS, set export extent using hydro dem
# set extent to the smaller dem (hydro one)
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -te -6490500 -1937000 3519500 4780000 -te_srs ESRI:102004 ./dems/7-5-arc-second-merged-500m-width-reproject-102004.tif ./dems/7-5-arc-second-merged-500m-width-reproject-102004-extent-matched.tif -r cubicspline -multi -co COMPRESS=ZSTD -co PREDICTOR=2 -co NUM_THREADS=ALL_CPUS -wo "NUM_THREADS=ALL_CPUS"

#create version of land dem with locations that are <=0 (but covered by hydro) raised to 1 elevation
python gdal_calc.py -A ./dems/7-5-arc-second-merged-500m-width-reproject-102004-extent-matched.tif -B ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm.tif --outfile ./dems/7-5-arc-second-500m-width-hydro-raised-above-sea-level-102004.tif --calc="(A > 0) * A + logical_and(A <= 0, B > 0) * 1 + logical_and(A <= 0, B <= 0) * A" --overwrite --co="COMPRESS=ZSTD" --co "PREDICTOR=2" --co NUM_THREADS=ALL_CPUS

# maritime version - lake add
#see waterboundaries.txt for commands
# add r.lake results to hydro-raised to 1 DEM. Locations that are still <=0 (but marked by lake) are raised (set) to 1 elevation
#avoid for -9999 nodata! if -dstnodata is used to set -9999 nodata, the gdalcalc will ignore all points that are in the -9999 nodata input!
python gdal_calc.py -A ./dems/7-5-arc-second-500m-width-hydro-raised-above-sea-level-102004.tif -B ./dissolved_500k/7-5-arc-second-ocean-500m-width-reproject-102004-extent-matched.tif --outfile ./dems/7-5-arc-second-500m-width-hydro-raised-above-sea-level2-102004.tif --calc="(A > 0) * A + logical_and(A <= 0, B < 0) * 1 + logical_and(A <= 0, B >= 0) * A" --overwrite --co="COMPRESS=ZSTD" --co "PREDICTOR=2" --co NUM_THREADS=ALL_CPUS

#raise nonhydro locations of 500x500 land dem. 
# Raise locations with no hydro and (>4m by 460m)/(>0, <=4 by scaled version to 460m at 4m). 
# Keep locations under hydro and 0m unchanged. 
# Accentuate coastlines and areas under 4m. Deepen stream paths vs surroundings so we can print more glow material for sufficient brightness. This also emphasizes below sea level areas. Displayed river width is due to 500mx500m resolution hydro DEM and diagonals and turns end up as 2500mx2500m. 
python gdal_calc.py -A ./dems/7-5-arc-second-merged-500m-width-reproject-102004-extent-matched.tif -B ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm.tif --outfile ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-raised-460.tif --calc="logical_and(B == 0, A > 4) * (A+460) + (B > 0) * A + logical_and(B == 0, A <= 0) * A + logical_and(B == 0, logical_and(A > 0, A <= 4)) * (A + A * 115)" --co="COMPRESS=ZSTD" --co "PREDICTOR=2" --co NUM_THREADS=ALL_CPUS

#raise nonhydro locations of 500x500 hydro fixed (raised) land dem. 
# Raise locations >4m by 400m (400m ensures that this area will be just below the previous DEM that has areas surrounding water artificially raised by 460m). This DEM should not poke above the previous DEM unless we display water there (because the previous DEM did not raise the water areas).
# Raise location >0,<=4m AND has water over it, <=4m by scaled amount to (114) at 4m. These areas will poke above the previous DEM in areas with water since we did not raise them in previous DEM. If no water there, leave unchanged so we don't poke above previous DEM in low areas with no hydro.
python gdal_calc.py -A ./dems/7-5-arc-second-500m-width-hydro-raised-above-sea-level-102004.tif -B ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm.tif --outfile ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-hydro-patched-raised-400.tif --calc="(A > 4) * (A+400) + (A<=0) * A + logical_and(A > 0, A<= 4) * (A + A * ((B > 0) * (14) + 100))" --co="COMPRESS=ZSTD" --co "PREDICTOR=2" --co NUM_THREADS=ALL_CPUS

#maritime version
python gdal_calc.py -A ./dems/7-5-arc-second-500m-width-hydro-raised-above-sea-level2-102004.tif -B ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm.tif --outfile ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-hydro-patched-raised2-400.tif --calc="(A > 4) * (A+400) + (A<=0) * A + logical_and(A > 0, A<= 4) * (A + A * ((B > 0) * (14) + 100))" --co="COMPRESS=ZSTD" --co "PREDICTOR=2" --co NUM_THREADS=ALL_CPUS

#run generate-gdal-commands.py
#run ./gdalwarp-batch.sh
#run generate-touch-terrain-config.py
#run touch-terrain-batch.sh
#comment AK out of libigl-boolean-subtract.sh
#run libigl-boolean-subtract.sh


#gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/DE.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-raised-850.tif ./dems/7-5-arc-second-clipped-500m/DE.tif -r cubicspline -multi -dstnodata -9999

#gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/DE.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-hydro-fixed-raised-800.tif ./dems/7-5-arc-second-clipped-500m-hydro-raised/DE-hydro-raised.tif -r cubicspline -multi -dstnodata -9999

#gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/MD.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-raised-850.tif ./dems/7-5-arc-second-clipped-500m/MD.tif -r cubicspline -multi -dstnodata -9999

#gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/MD.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/7-5-arc-second-merged-500m-width-hydro-fixed-raised-800.tif ./dems/7-5-arc-second-clipped-500m-hydro-raised/MD-hydro-raised.tif -r cubicspline -multi -dstnodata -9999

#old method
#gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/SC.gpkg -crop_to_cutline ./dems/7-5-arc-second-merged.tif ./dems/7-5-arc-second-clipped-500m/SC.tif -r cubicspline -multi -dstnodata -9999
#gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/SC.gpkg -crop_to_cutline ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_merged_100m_ge_10sqkm.tif C:/Users/ansonl/development/dem-to-stl-workflow/dems/stream-lake-mask-clipped-500m/SC.tif -r cubicspline -multi


#gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/SC.gpkg -crop_to_cutline ./dems/7-5-arc-second-clipped-500m/SC.tif ./dems/7-5-arc-second-clipped-500m/SC2.tif -r cubicspline -multi -dstnodata -9999