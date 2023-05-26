#merge SRTM
gdalbuildvrt -resolution highest -overwrite north_america_srtm_wgs84.vrt SRTM/*.hgt
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2"-co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_srtm_wgs84.vrt north_america_srtm_wgs84.tif

#merge GMTED
gdalbuildvrt -resolution highest north_america_gmted2010_wgs84.vrt GMTED2010/7-5-arc-second/mea/*.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_gmted2010_wgs84.vrt north_america_gmted2010_wgs84.tif

#merge GMTED and SRTM buildvrt
gdalbuildvrt -resolution highest -overwrite north_america_gmted2010_srtm_merge.vrt north_america_gmted2010_wgs84.tif north_america_srtm_wgs84.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_gmted2010_srtm_merge.vrt north_america_gmted2010_srtm_merge.tif

#merge GMTED and SRTM buildvrt and warp to 102004
gdalwarp -overwrite -t_srs ESRI:102004 -r average  -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE" north_america_gmted2010_srtm_merge.vrt north_america_gmted2010_srtm_merge_102004.tif

#use merged GMTED and SRTM TIF in WGS84 and warp to 102004 and downscale to 500x500m with bilinear/average resampling (doing it in QGIS>export>save as does not seem to have gaps if reproject and downscale at same time)
gdalwarp -overwrite -t_srs ESRI:102004 -tr 500.0 500.0 -r average -multi -of GTiff -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=FALSE" north_america_gmted2010_srtm_merge.tif north_america_gmted2010_srtm_merge_102004_500m_average.tif

#upscale to 250x250m
gdalwarp -overwrite -t_srs ESRI:102004 -tr 250.0 250.0 -r bilinear -multi -of GTiff -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=FALSE" north_america_gmted2010_srtm_merge_102004_500m_average.tif north_america_gmted2010_srtm_merge_102004_500m_avg_250m_bi.tif

#test upscale in cubicspline
gdalwarp -overwrite -t_srs ESRI:102004 -tr 250.0 250.0 -r cubicspline -multi -of GTiff -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=FALSE" north_america_gmted2010_srtm_merge_102004_500m_average.tif north_america_gmted2010_srtm_merge_102004_500m_avg_250m_cubicspline.tif