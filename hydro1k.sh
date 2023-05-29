#buffer at 1k width 
#rasterize 250x250m
#export in 102004

# Upsample rasterized source hydro1k to 1500x1500m resolution
# source resolution 25x25m
# output resolution 750x750m

# 25x25 > 1000x1000 > 750x750 > 500x500

#gdalwarp -overwrite -of GTiff -tr 1500.0 1500.0 ./sources/hydro1k_mask_25m_102004.tif ./hydrographic-masks/hydro1k_mask_1250m_102004.tif -r max -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"

#gdalwarp -overwrite -of GTiff -tr 750.0 750.0 ./hydrographic-masks/hydro1k_mask_1250m_102004.tif ./hydrographic-masks/hydro1k_mask_750m_102004.tif -r max -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"

#gdalwarp -overwrite -of GTiff -tr 250.0 250.0 ./hydrographic-masks/hydro1k_mask_750m_102004.tif ./hydrographic-masks/hydro1k_mask_250m_102004.tif -r bilinear -multi -co "TILED=YES" -co "COMPRESS=ZSTD" -co "PREDICTOR=2" -co "BIGTIFF=IF_SAFER" -co "NUM_THREADS=ALL_CPUS" -wo "NUM_THREADS=ALL_CPUS" -wo "USE_OPENCL=TRUE"
