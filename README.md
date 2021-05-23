# Clipped DEM to STL workflow

```
Data working directory file structure details

>geographic-data
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

Requires TouchTerrain to be available in the Python environment. 

1. Split census US state boundary shapefile into individual states' files
  - QGIS > Vector > Data Management > Split
    - Split state boundary file to individual files using STUSPS column. Save state files to `boundaries` folder.
    - Modify below Python snippet's `os.chdir` call parameter to `boundaries` folder path. 
    - Run below Python snippet in QGIS > Plugins > Python Console to remove "STUSPS_" prefix in resulting boundary files.
    ```
import os
os.chdir("C:/Users/ansonl/development/mapConstraintColorizer/geographic-data/boundaries")
for fileName in os.listdir("."):
	os.rename(fileName, fileName.replace("STUSPS_", ""))
    ```

2. Merge all DEM files
  - QGIS > Raster > Miscellaneous > Merge
    - Merge all DEM files to one file
    - USGS DEM GMTED2010 CRS is WGS84 -> Keep as WGS84
    - Save in `dems` folder. Example file name if using 30 arc second data is `30-arc-second-merged.tif`

3. Downscale merged USA DEM file
  - Right click the DEM layer > Export > Save as > specify X and Y resolution of 1000 with the output CRS set to USA Contiguous Lambert Conformal Conic. For some reason I needed to set it from North America -> USA Contiguous to switch the "Save Raster Layer as" tool units from degrees to meters so that the output resolution can be set to 1000 (m) in both X and Y. 
  - Set 1000m USA DEM CRS back to North America Lambert Conformal Conic 

4. Split state boundary vector file into individual state boundary vector files
  - QGIS > Split vector layer
    - Use STUSPS as key
      
5. Clip 1000m DEM by each state boundary
  - QGIS > Clip raster by mask layer
    - Batch process
    - Input raster: 1000m DEM from step 3
    - Input mask layer: Every state boundary file
    - Target CRS: North America Lambert Conformal Conic
    - Output file: "clip_" + use parameter name (input mask layer)
    - Save under `dems/1000m-clipped` directory
    - Remove `clip_` prefix from saved files' filenames (see below sample Python snippet)
    ```
import os
os.chdir("C:/Users/ansonl/development/mapConstraintColorizer/geographic-data/dems/1000m-clipped")
for fileName in os.listdir("."):
	os.rename(fileName, fileName.replace("clip_", ""))
    ```

6. Generate TouchTerrain configurations and commands and batch 3D model generation script using `generate-touch-terrain-config.py` either in the terminal, Spyder, or QGIS > Processing > Python console. .

7. Generate state STL 3D models
  - Modify `Pool(N)` in `touch-terrain-batch-python-multithread.py` to the number of threads to use to generate 3D models.
  - Run `touch-terrain-batch-python-multithread.py` in the terminal or Spyder.

#### Setting zero DEM values to NODATA before saving DEMs.
*This is unneeded if using TouchTerrain config parameter `ignore_leq` to generate STLs*
  -Run batch graphical modeler script (set-zero-to-nodata.model3) to replace all points with elevation <= 0 with NODATA in all clipped state.tif files
    - Prepend resulting filename with "nodata_" and append with Input_Raster.
    - Use Lambert Conformal Conic projection system as CRS
    - Save new nodata files in `tmp/nodata` folder

