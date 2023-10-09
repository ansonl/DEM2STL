# DEM to STL workflow
Convert DEMs with complex boundaries to STL models in preparation for 3D printing.

```
Data working directory file structure details

>geographic-data (root)
	-README.md
	-set-zero-to-nodata.model3 <- QGIS process model for setting zero values to NODATA
	-touch-terrain-batch-python-multithread.py <- Interpretation and multithreaded execution of generated touch-terrain-batch.sh
	>boundaries
	  -XX.gpkg <- XX boundaries
	>dems
	  -30-arc-second-merged.tif <-merged North America DEM from step 2
	  >1000m-clipped
	    -XX.tif <- XX DEM
	>state_stls <- generated state stl files
	  -example_config.json
	  -TouchTerrain_standalone.py
	  -touch-terrain-batch.sh <- generated batch script to run Touch Terrain
	>touch_terrain_configs
	  -XX.json <-generated config JSON file for each state
```

Recommended setup is setting up a Python 3 virtual environment through Anaconda with the root of the virtual environment set to the `geographic-data` directory. 

Requires [TouchTerrain](https://github.com/ChHarding/TouchTerrain_for_CAGEO) v3.3+ to be available in the Python environment. Use TouchTerrain `setup.py` file to [set up TouchTerrain](https://github.com/ChHarding/TouchTerrain_for_CAGEO) in the environment. 

1. Split census US state boundary shapefile into individual states' files
- QGIS > Vector > Data Management > Split
  - Split state boundary file to individual files using STUSPS column. Save state files to `boundaries` folder.
  - Modify below Python snippet's `os.chdir` call parameter to `boundaries` folder path. 
  - Run below Python snippet in QGIS > Plugins > Python Console to remove "STUSPS_" prefix in resulting boundary files.

```
import os
os.chdir("C:/Users/ansonl/development/dem-to-stl-workflow/dem/boundaries")
for fileName in os.listdir("."):
  print(fileName)
  os.rename(fileName, fileName.replace("STUSPS_", ""))
```

2. Merge all DEM files
- QGIS > Raster > Miscellaneous > Merge
  - Use *dsc* (Systematic Subsample) DEMs from GMTED2010
  - Remove *non-dsc* tifs in DEM directory with
```
shopt -s extglob
rm -if !(*.zip|*dsc*.tif)
shopt -u extglob
```
  - Merge all DEM files to one file
  - USGS DEM GMTED2010 CRS is WGS84 -> Keep as WGS84
  - Save in `dems` folder. Example file name if using 30 arc second data is `30-arc-second-merged.tif`

3. Downscale merged USA DEM file
- Right click the DEM layer > Export > Save as > specify X and Y resolution of 1000 with the output CRS set to USA Contiguous Lambert Conformal Conic. For some reason I needed to set it from North America -> USA Contiguous to switch the "Save Raster Layer as" tool units from degrees to meters so that the output resolution can be set to 1000 (m) in both X and Y. (or 100m resolution)
- Set 1000m USA DEM CRS back to North America Lambert Conformal Conic 

4. Split state boundary vector file into individual state boundary vector files
- QGIS > Split vector layer
  - Use STUSPS as key
  - Use python snippet below to remove STUSPS prefix from the individual state files
```
import os
os.chdir("C:/Users/ansonl/development/dem-to-stl-workflow/cb_2019_us_states_individual")
for fileName in os.listdir("."):
  os.rename(fileName, fileName.replace("STUSPS_", ""))
```
    
5. Clip 1000m DEM by each state boundary OR use `generate-gdal-commands.py` `gdal-batch-python-multithread.py` to clip both DEM and mask files. 
- QGIS > Clip raster by mask layer
- If using a offset mask layer DEM for 3D model generation, both base and offset layer should be reprojected to the same CRS and downscaled to the same pixel size (ex:1000\[m\])
  - Batch process
  - Input raster: 1000m DEM from step 3
  - Input mask layer: Every state boundary file
  - Target CRS: North America Lambert Conformal Conic
  - Must specify output resolution: YES X:1000 Y:1000 (if 1000m scale) to ensure base and offset layers have same dimensions.
  - Clipped (mask) (Output file): 'clip_' + use parameter name (input mask layer)
    - Save under `dems/1000m-clipped` directory
  - Remove `clip_` prefix from saved files' filenames (see below sample Python snippet)

```
import os
os.chdir("C:/Users/ansonl/development/dem-to-stl-workflow/dems/7-5-arc-second-1000m-clipped")
for fileName in os.listdir("."):
  os.rename(fileName, fileName.replace("clip_", ""))
```
```
import os
os.chdir("C:/Users/ansonl/development/dem-to-stl-workflow/dems/1000m-clipped")
for fileName in os.listdir("."):
  os.rename(fileName, fileName.replace("clip_", ""))
```

6. Generate TouchTerrain configurations and commands and batch 3D model generation script using `generate-touch-terrain-config.py` either in the terminal, Spyder, or QGIS > Processing > Python console.

7. Generate state STL 3D models
- Modify `Pool(N)` in `touch-terrain-batch-python-multithread.py` to the number of threads to use to generate 3D models.
- Run `touch-terrain-batch-python-multithread.py` in the terminal or Spyder.

### Setting zero DEM values to NODATA before saving DEMs.
*This is unneeded if using TouchTerrain config parameter `ignore_leq` to generate STLs*
- Run batch graphical modeler script `set-zero-to-nodata.model3` to replace all points with elevation <= 0 with NODATA in all clipped state.tif files
  - Prepend resulting filename with "nodata_" and append with Input_Raster.
  - Use Lambert Conformal Conic projection system as CRS
  - Save new nodata files in `tmp/nodata` folder

### Installing USGS Bulk Download tool.
- Bulk Download requires BOTH Java Runtime Environment (JRE) and Java Development Kit (JDK) to be installed. 

### Creating offset mask layer Hydro1k and HydroLAKES

1. Reproject Hydro1k and HydroLAKES vectors to projection mode of map (102004 lambert)

2. Rasterize Hydro1k and HydroLAKES vector layers using a constant value
  - QGIS>GDAL>Vector conversion>Rasterize (vector to raster). Set to georeferenced units and set resolutions relative to vector unit of measurement
  - Use Int16 or smallest signed data format since we are just making a mask
  - Constant value = 1
  - No data = 0
  - georeferenced units relative to source layer units (If the source layer is in a projected CRS, source layer units should be meters. )
  - extent set to source layer extent
  - If you want to decrease noise from small lakes, filter the projected vector in QGIS with "Lake_area" >= 10 to only show lakes with over 10sqkm of area.
    - Select by Expression  
    - if( "Lake_area"  / "Shore_len" > 0.5, if( "Lake_area" > 9, true, if( "Shore_len" > 24, true, if( "Wshd_area" > 1000, if( "Lake_area" > 6.5, true, false), false))), if( "Lake_area" > 10, true, if( "Shore_len" > 24, true, if( "Wshd_area" > 1000, if( "Lake_area" > 6.5, true, false), false))))
  2a. Clip Hydro1k and HydroLAKES vector layers using USA boundary polygon.
    - QGIS>GDAL>Raster Extraction>Clip raster by mask layer
    - Clipping may need to be done on the raster rather than the vector due to state boundary polygon incompatibility in QGIS.

3. Translate Hydro1k and HydroLAKES no data value from 0 to -1
  - Save both output raster mask layers for future reference. (Recommended)
  - replace nodata values with 0 with RAster>Conversion>Translate. Use -1 as nodata value. Now no data values that were 0 in the raster are now really "0". 
  - https://gis.stackexchange.com/a/298251/131082

4. Combine stream and lake raster mask layers to get a raster layer with lakes and streams highlighted.
  - QGIS>Raster>Raster Calculator
  - Pick extent and resolution in a projected CRS that matches the desired output. Width and height resolution will be autofilled. This needs to have the same resolution as real region DEMs that will be offset so that vector array add in numpy will work.
  - e.g. `"hydro1k_mask@1" + ("hydro1k_mask@1" != 1) * "hydrolakes@1"`

5. Clip raster by mask layer using Batch Processing to create offset mask layer for each state's polygon.

6. Truncate prefix added by QGIS batch processing.
```
import os
os.chdir("C:/Users/ansonl/development/dem-to-stl-workflow/dems/stream-lake-mask-clipped-500m")
for fileName in os.listdir("."):
  os.rename(fileName, fileName.replace("clipSTUSPS_", ""))

```

# scratch pad

>ogr2ogr -f "GPX" sc_streams2.gpx -t_srs "ESRI:102009" sc_streams.gpx
>gdalinfo ../dems/1000m-clipped/SC.tif

For perfect border fit, the printres=-1
DEM pixel res 1000mx1000m, clip res 1000 1000

python gdal_calc.py -A ./dems/7-5-arc-second-clipped-500m/MD.tif -B ./dems/stream-lake-mask-clipped-500m/MD.tif --outfile ./dems/7-5-arc-second-clipped-500m/MD-low-hydro-to-above-sealevel.tif --calc="A*(A>0)+(A<=0)*(B>-1)*(B<1)*1"

gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/MD.gpkg -crop_to_cutline ./dems/7-5-arc-second-merged.tif ./dems/7-5-arc-second-clipped-500m/MD.tif -r cubicspline -multi -dstnodata -9999

# raise hydro locations that are below or at sea level to 1. Both input tif must be in same CRS/projection!
# Use QGIS Raster Calc if resolution of two inputs are not the same. Translate generated file datatype to Int16 (or matching non-hydro raised file datatype) before export. This will prevent non-PWN error when doing boolean subtraction in libigl with touchterrain generated file. Changing Float32 to Int16 also fixes a rounding issue where locations that should be 0 are a very small number and touchterrain generates them as land (not good for printing).
python gdal_calc.py -A ./dems/7-5-arc-second-merged-reproject-102004.tif -B ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm.tif --outfile ./dems/7-5-arc-second-500m-width-hydro-raised-above-sea-level-102004.tif --calc="(A > 0) * A + (A <= 0 AND B > 0) * 1 + (A <= 0 AND B <= 0) * A"

("7-5-arc-second-merged-reproject-102004@1" > 0) * "7-5-arc-second-merged-reproject-102004@1" + ("7-5-arc-second-merged-reproject-102004@1" <= 0 AND "usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm@1" > 0) * 1 + ("7-5-arc-second-merged-reproject-102004@1" <= 0 AND "usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm@1" <= 0) * "7-5-arc-second-merged-reproject-102004@1"

"(A > 0) * A + (A <= 0 AND B > 0) * 1 + (A <= 0 AND B <= 0) * A"

# create 500x500m version of north american hydrolakes merged because the 100x100m version lines are too narrow to raise any sea level hydro areas. Float32 data type is ok.
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_merged_100m_ge_10sqkm.tif C:/Users/ansonl/development/dem-to-stl-workflow/usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_500m_ge_10sqkm.tif -r cubicspline -multi

gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 1000.0 1000.0 -tap ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_merged_100m_ge_10sqkm.tif C:/Users/ansonl/development/dem-to-stl-workflow/usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_warp_1000m_ge_10sqkm.tif -r cubicspline -multi

gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/MD.gpkg -crop_to_cutline ./dems/7-5-arc-second-merged-reproject-102004.tif ./dems/7-5-arc-second-clipped-500m/MD.tif -r cubicspline -multi -dstnodata -9999
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/MD.gpkg -crop_to_cutline ./usa_hydro1k_hydrolakes_merged/usa_hydro1k_hydrolakes_merged_100m_ge_10sqkm.tif C:/Users/ansonl/development/dem-to-stl-workflow/dems/stream-lake-mask-clipped-500m/MD.tif -r cubicspline -multi
gdalwarp -overwrite -t_srs ESRI:102004 -of GTiff -tr 500.0 500.0 -tap -cutline ./cb_2018_us_state_20m_individual/MD.gpkg -crop_to_cutline ./dems/7-5-arc-second-1000m-width-hydro-raised-above-sea-level-102004.tif ./dems/7-5-arc-second-clipped-500m-hydro-raised/MD-hydro-raised.tif -r cubicspline -multi -dstnodata -9999

./gp-cli/precompiled/pc/bin/meshboolean.exe ./state_stls/MD-no-rivers/MD-hydro-raised_tile_1_1.STL ./state_stls/MD/MD_tile_1_1.STL minus ./state_stls/MD/MD_rivers.STL


### License

- All files are released under [GNU Affero General Public License](https://www.gnu.org/licenses/gpl-faq.html). Copyright Anson Liu.
  - File `TouchTerrain_standalone.py` is provided for convenience. It is from the [TouchTerrain](https://github.com/ChHarding/TouchTerrain_for_CAGEO) project.  

- Commercial support is available as a consulting service. 

- Commercial licensing is required for any usage that does not comply with AGPL. This includes nonattributed commercial distribution of models created using this code.

- Contact support@ansonliu.com for commercial support and licensing. 
