#crop to usa48
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 10000 10000 -cutline ../../sources/USCB/USCB2018/cb_2018_us_state_5m/usa48.gpkg -crop_to_cutline ../../sources/north_america_gmted2010_srtm_merge_102004_1000m_avg_250m_cubicspline.tif ./usa_48_102004_2500m_cubicspline.tif -r cubicspline -multi

mkdir ./globalLogScaleLandA/
mkdir ./touch_terrain_configs_20m/
mkdir ./state_stls_20m/
mkdir ./tmp/state_stls_20m/

$env:PYTHONPATH = './'

#create VRT for globalLogScaleLandA
gdalbuildvrt -resolution lowest -overwrite globalLogScaleLandA.vrt usa_48_102004_2500m_cubicspline.tif
python ../../workflow/patchVRT.py globalLogScaleLandA.vrt globalLogScaleLandA
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" globalLogScaleLandA.vrt ./globalLogScaleLandA/usa-48-log.tif --config GDAL_VRT_ENABLE_PYTHON YES

python ..\..\generate-touch-terrain-config.py usa-48-log-low-poly

python ../../TouchTerrain_standalone.py ./touch_terrain_configs_20m/usa-48-log-low-poly.json

#decimate modifier
# collapse