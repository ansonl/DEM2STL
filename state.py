import geopandas as gpd
input_file = "./tl_2022_us_state/split_individual/ME.gpkg"
data = gpd.read_file(input_file)
data.head().bounds
convertedData = data.to_crs('ESRI:102004')
convertedData.head().bounds

#get state extent
print(convertedData.total_bounds)

import math
# extend state extents by 5000m in each direction which is 10 (500x500) pixels
print([math.floor(convertedData.total_bounds[0]-5000), math.floor(convertedData.total_bounds[1]-5000), math.ceil(convertedData.total_bounds[2]+5000), math.ceil(convertedData.total_bounds[3]+5000)])
# ME [1925836.2845578345, 715547.1196991404, 2268720.5956089958, 1251148.1439610166]

# do gdal crop of raw strm and gmtopo to extended state extent
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 20.0 20.0 -te 1925836.2845578345 715547.1196991404 2268720.5956089958 1251148.1439610166 -te_srs ESRI:102004 ./dems/7-5-arc-second-merged-reproject-102004.tif ./dems/tmp/gmted-ME.tif -r cubicspline -multi -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 20.0 20.0 -te 1925836.2845578345 715547.1196991404 2268720.5956089958 1251148.1439610166 -te_srs ESRI:102004 ./srtm/north_america_srtm.tif ./dems/tmp/srtm-ME.tif -r cubicspline -multi -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

# combine state gmted and srtm, keep srtm where they overlap
python gdal_calc.py -A ./dems/tmp/gmted-ME.tif -B ./dems/tmp/srtm-ME.tif --outfile ./dems/tmp/combined-ME.tif --calc="A + B - (logical_and(B > 0, B<= 0) * A)" --overwrite --co="COMPRESS=ZSTD" --co "PREDICTOR=2" --co "NUM_THREADS=ALL_CPUS"

#or mosaic (do not -tap or it will shift pixels)
python gdal_merge.py -o ./dems/tmp/mosaic-ME.tif -of GTiff -co COMPRESS=ZSTD -co PREDICTOR=2 -co BIGTIFF=YES -co NUM_THREADS=ALL_CPUS -ps 20.0 20.0 -v ./dems/tmp/gmted-ME.tif ./dems/tmp/srtm-ME.tif

#or buildvrt
gdalbuildvrt -resolution highest -overwrite north_america_gmted_srtm_merge.vrt north_america_gmted-7-5-arc-second_wgs84.tif north_america_srtm_wgs84.tif

#set cache size to 9999mb before running anything
set GDAL_CACHEMAX=9999

#merge SRTM
gdalbuildvrt -resolution highest -overwrite north_america_srtm_wgs84.vrt SRTM/*.hgt
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2"-co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_srtm_wgs84.vrt north_america_srtm_wgs84.tif

#merge GMTED
gdalbuildvrt -resolution highest north_america_gmted2010_wgs84.vrt GMTED2010/7-5-arc-second/mea/*.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_gmted2010_wgs84.vrt north_america_gmted2010_wgs84.tif

#merge GMTED and SRTM buildvrt
gdalbuildvrt -resolution highest -overwrite north_america_gmted2010_srtm_merge.vrt north_america_gmted2010_wgs84.vrt north_america_srtm_wgs84.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_gmted2010_srtm_merge.vrt north_america_gmted2010_srtm_merge.tif

#clip merged at -180,-60,15,72 [EPSG:4326]

#test vrt crop speed
gdalwarp -overwrite -of GTiff -te 1925836.2845578345 715547.1196991404 2268720.5956089958 1251148.1439610166 -te_srs ESRI:102004 north_america_gmted_srtm_merge.vrt merged_vrt_ME.tif -multi -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

COMPRESS=ZSTD,PREDICTOR=2,BIGTIFF=YES,TILED=YES,NUM_THREADS=ALL_CPUS

#gdal_merge.py has error when merging entire USA
#grass i.image.mosaic does resampling which decreases quality since we have already resampled in our upscaling
#gdal_merge.py effect is identical to grass i.image.patch so use patch in QGIS on USA

processing.run("grass7:r.patch", {'input':['C:/Users/ansonl/development/dem-to-stl-workflow/dems/tmp/srtm-ME.tif','C:/Users/ansonl/development/dem-to-stl-workflow/dems/tmp/gmted-ME.tif'],'-z':False,'output':'TEMPORARY_OUTPUT','GRASS_REGION_PARAMETER':None,'GRASS_REGION_CELLSIZE_PARAMETER':0,'GRASS_RASTER_FORMAT_OPT':'COMPRESS=ZSTD,PREDICTOR=2,BIGTIFF=YES,NUM_THREADS=ALL_CPUS','GRASS_RASTER_FORMAT_META':''})

#run lake here

#downscale lake output to 500x500m resolution and crop
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -te 1925836.2845578345 715547.1196991404 2268720.5956089958 1251148.1439610166 -te_srs ESRI:102004 -tap ./dissolved_500k/lake-ME.tif ./dissolved_500k/lake-ME-500m.tif -r cubicspline -multi -co COMPRESS=ZSTD -co PREDICTOR=2 -co NUM_THREADS=ALL_CPUS -wo "NUM_THREADS=ALL_CPUS"

#watch out for -9999 nodata, if -dstnodata is used to set -9999 nodata, the gdalcalc will ignore all points that are in the -9999 nodata input!

### start normal processing but with the state

#downscale state land dem to 500x500m resolution
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -te 1925836.2845578345 715547.1196991404 2268720.5956089958 1251148.1439610166 -te_srs ESRI:102004 -tap ./dems/tmp/mosaic-ME.tif ./dems/tmp/mosaic-ME-500m.tif -r cubicspline -multi -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" 

#crop hydrolakes to state dem
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -te 1925836.2845578345 715547.1196991404 2268720.5956089958 1251148.1439610166 -te_srs ESRI:102004 -tap ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm.tif ./dems/tmp/hydro-ME.tif -r cubicspline -multi -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS"

#create version of land dem with locations that are <=0 (but covered by hydro) raised to 1 elevation
python gdal_calc.py -A ./dems/tmp/mosaic-ME-500m.tif -B ./dems/tmp/hydro-ME.tif --outfile ./dems/tmp/ME-500m-width-hydro-raised-above-sea-level-102004.tif --calc="(A > 0) * A + logical_and(A <= 0, B > 0) * 1 + logical_and(A <= 0, B <= 0) * A" --overwrite --co=COMPRESS=ZSTD --co=PREDICTOR=2 --co=NUM_THREADS=ALL_CPUS

# maritime version - lake add
#see waterboundaries.txt for commands
# add r.lake results to hydro-raised to 1 DEM. Locations that are still <=0 (but marked by lake) are raised (set) to 1 elevation
#avoid for -9999 nodata! if -dstnodata is used to set -9999 nodata, the gdalcalc will ignore all points that are in the -9999 nodata input!
python gdal_calc.py -A ./dems/tmp/ME-500m-width-hydro-raised-above-sea-level-102004.tif -B ./dissolved_500k/lake-ME-500m.tif --outfile ./dems/tmp/ME-500m-width-hydro-raised-above-sea-level2-102004.tif --calc="(A > 0) * A + logical_and(A <= 0, B < 0) * 1 + logical_and(A <= 0, B >= 0) * 1" --overwrite --co=COMPRESS=ZSTD --co=PREDICTOR=2 --co=NUM_THREADS=ALL_CPUS

#raise nonhydro locations of 500x500 land dem. 
# Raise locations with no hydro and (>4m by 460m)/(>0, <=4 by scaled version to 460m at 4m). 
# Keep locations under hydro and 0m unchanged. 
# Accentuate coastlines and areas under 4m. Deepen stream paths vs surroundings so we can print more glow material for sufficient brightness. This also emphasizes below sea level areas. Displayed river width is due to 500mx500m resolution hydro DEM and diagonals and turns end up as 2500mx2500m. 
python gdal_calc.py -A ./dems/tmp/mosaic-ME-500m.tif -B ./dems/tmp/hydro-ME.tif --outfile ./dems/dems-ready-to-cut/ME-500m-width-raised-460.tif --calc="logical_and(B == 0, A > 4) * (A+460) + (B > 0) * A + logical_and(B == 0, A <= 0) * A + logical_and(B == 0, logical_and(A > 0, A <= 4)) * (A + A * 115)" --overwrite --co=COMPRESS=ZSTD --co=PREDICTOR=2 --co=NUM_THREADS=ALL_CPUS

#raise locations of 500x500 hydro fixed (raised) land dem. 
# Raise locations >4m by 400m (400m ensures that this area will be just below the previous DEM that has areas surrounding water artificially raised by 460m). This DEM should not poke above the previous DEM unless we display water there (because the previous DEM did not raise the water areas).
# Raise location >0,<=4m AND has water over it, <=4m by scaled amount to (114) at 4m. These areas will poke above the previous DEM in areas with water since we did not raise them in previous DEM. If no water there, leave unchanged so we don't poke above previous DEM in low areas with no hydro.
#python gdal_calc.py -A ./dems/tmp/ME-500m-width-hydro-raised-above-sea-level-102004.tif -B ./dems/tmp/hydro-ME.tif --outfile ./dems/dems-ready-to-cut/ME-500m-width-hydro-patched-raised-400.tif --calc="(A > 4) * (A+400) + (A<=0) * A + logical_and(A > 0, A<= 4) * (A + A * ((B > 0) * (14) + 100))" --overwrite --co="COMPRESS=ZSTD" --co "PREDICTOR=2" --co NUM_THREADS=ALL_CPUS

#maritime version
python gdal_calc.py -A ./dems/tmp/ME-500m-width-hydro-raised-above-sea-level2-102004.tif -B ./dems/tmp/hydro-ME.tif --outfile ./dems/dems-ready-to-cut/ME-500m-width-hydro-patched-raised2-400.tif --calc="(A > 4) * (A+400) + (A<=0) * A + logical_and(A > 0, A<= 4) * (A + A * ((B > 0) * (14) + 100))" --overwrite --co="COMPRESS=ZSTD" --co "PREDICTOR=2" --co NUM_THREADS=ALL_CPUS


gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500 500 -tap -cutline ./tl_2022_us_state/split_individual/ME.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/ME-500m-width-raised-460.tif ./dems/7-5-arc-second-clipped-500m/ME.tif -r cubicspline -multi -dstnodata -9999
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500 500 -tap -cutline ./tl_2022_us_state/split_individual/ME.gpkg -crop_to_cutline ./dems/dems-ready-to-cut/ME-500m-width-hydro-patched-raised2-400.tif C:/Users/ansonl/development/dem-to-stl-workflow/dems/7-5-arc-second-clipped-500m-hydro-patched/ME-hydro-patched.tif -r cubicspline -multi

