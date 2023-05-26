#convert all masks to wgs84 for merge
#gdalwarp -overwrite -t_srs ESRI:102004 -r bilinear -of GTiff -co COMPRESS=ZSTD -co PREDICTOR=2 -co NUM_THREADS=ALL_CPUS -co BIGTIFF=IF_SAFER -co TILED=YES ./hydrolakes_mask_gt10sqkm_wgs84.tif ./hydrolakes_mask_gt10sqkm_102004.tif

#merge all coastline masks
gdalbuildvrt -resolution highest -overwrite coastline_hydrographic_mask_merge.vrt coastline/*.tif
# set VRT data type from Float32 to Int16
gdal_translate -ot Int16 coastline_hydrographic_mask_merge.vrt coastline_hydrographic_mask_merge_int16.vrt

#merge coastline, hydro1k, hydrolakes masks
gdalbuildvrt -resolution highest -overwrite north_america_hydrographic_mask_merge.vrt coastline_hydrographic_mask_merge_int16.vrt hydro1k_mask_500m_wgs84.tif hydrolakes_mask_gt10sqkm_wgs84.tif
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_hydrographic_mask_merge.vrt north_america_hydrographic_mask_merge.tif

#reproject to 102004
gdalwarp -overwrite -t_srs ESRI:102004 north_america_hydrographic_mask_merge.vrt  north_america_hydrographic_mask_merge_102004.vrt -r near -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
#gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff north_america_hydrographic_mask_merge.tif north_america_hydrographic_mask_merge_102004.tif -r cubic -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"

#downscale to 250x250m
gdalwarp -overwrite -tr 250.0 250.0 north_america_hydrographic_mask_merge_102004.vrt north_america_hydrographic_mask_merge_102004_250m.vrt -r max -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
gdal_translate -ot Int16 -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" north_america_hydrographic_mask_merge_102004_250m.vrt north_america_hydrographic_mask_merge_102004_250m.tif