# REGION_NAME (REGION_ABBR) Topographic Relief Map with Rivers and Coastal Waters

REGION_NAME mountains, coastlines, streams, and lakes in a dual color topographic and hydrographic map! All topographic states in the [USA of Plastic](https://www.printables.com/@ansonl_365531/collections/714909) project interlock with each other like a puzzle.

Show off streams, lakes, and coastlines with filament that is glow-in-the-dark or translucent — or simply a different color from the base.

## Recommended Model Files for you to print? See 🌟 or ⭐ below

- REGION_ABBR-sqrt-dual.3mf 🌟 (Dual extrusion only ⚠️)
- REGION_ABBR-sqrt-single.3mf ⭐ (Single/Dual extrusion OK)

*Recommended to download only the model file name you need to avoid long download time and extra storage usage.*

## Model Filename Decoder

`STATE-ESCALING-VARIANT-STYLE-VERSION-PIECE##.3mf`

| Definition | Meaning |
| ---- | ---- |
| `STATE` | State Abbreviation |
| `ESCALING` | Linear or Square Root (sqrt) elevation scaling. |
| `VARIANT` | Dual or Single color model |
| `STYLE` *(optional)* | `STYLE` is only present when the model is a special style or the model is exclusive to a special subregion. Default style is water model printed over submerged low lying lands. This submerged land may be visible when water layers are printed with a transparent filament. Default style minimizes usage of secondary (water) filament color. `transparent` style is water model features go all the way through the land for max light transmission when used with glow and transparent filaments.|
| `VERSION` | Version number |
| `PIECE##` *(optional)* | Interlocking piece # for 180 mm x 180 mm bed |

All individual state 3D printable 3MF files are cut for your convenience and fit together once printed. The files are in 3MF format instead of STL for smaller file size and in order to store separate land and water objects that are aligned for accurate dual color prints. 3MF is supported in Cura, PrusaSlicer, and other 3D slicers. If you need the STL, you may convert the 3MF by importing+exporting in a 3D modeling program.

*If multi-part files are not present, I have not created interlocking models for this state yet. Follow me and comment with your request to get future additions and updates.*

# Recommended print settings

Print the models as is with a dual extrusion printer. If you have a single extrusion printer, you can either print the `*-single.3mf` model or run two single extrusion prints utilizing the Z-hop method on the water model.

You can scale the model up or down as needed to fit your printer size, the final map's scale will just be scaled accordingly. *E.g. 200% scale on a previous scale of **0.4mm:1000m** results in **0.4mm:500m***

Download the optimized Cura print settings profile for topo maps [HERE](https://www.printables.com/model/529276-contiguous-usa-lower-48-topographic-map-with-hydro). 

*Merging `(Ctrl+Alt+G)` objects before rotating and scaling (if needed) in Cura will help keep the dual color print objects aligned.*

Printing this will test your 3D printer's XY precision, Z-axis stability, retraction, cooling, and oozing!

| Slicer Setting | Recommended Value (0.4 mm nozzle) |
| ------------- |-------------|
| Layer Height | 0.1 mm |
| Line Width | 0.4 mm |
| Minimum Thin Wall Line Width | 0.2 mm |
| Top Surface Skin Layers | 2 |
| Top Surface Skin Pattern | Lines |
| Skin Overlap | 20% |
| Top/Bottom Flow | 100% |
| Top Surface Skin Flow | 100% |
| Infill and Infill Percentage | Lightning 30% |
| Ironing Line Spacing | 0.2 mm |
| Ironing Flow | 20% |
| Ironing Inset | 0.34 mm |
| Ironing Speed | 60 mm/s |
| Brim Extruder | Extruder 1 or 2 |
| Ooze Shield | Yes |

| Cartographic Specification | Value | Notes |
| ------------- | ------------- | ------------- |
| Projection | USA Contiguous Lambert Conformal Conic |
| Horizonal Scale | 1:2500000 (0.4mm:1000m) | Effective resolution is 1000m x 1000m. Territorial waters are included in the dual print models. |
| Vertical Scale | 1:500000 (0.1mm:50m) | Effective vertical exaggeration is 5x. Elevations 0-40m are scaled between 0 and 0.8mm on a logarithmic scale for enhanced coastal detail. |
| Maritime Boundary | Submerged Lands Act | Seaward boundary of coastal states generally 3 or 9 nm from the coastline. |

**Need a special location/map modeled and printed as a showpiece or gift?** [Contact me](mailto:maps@ansonliu.com) *([maps@ansonliu.com](mailto:maps@ansonliu.com))* for design and production services to bring your idea to life!

## Credits

USAofPlastic topographic map project uses data from [NASA SRTM V3.0](https://www2.jpl.nasa.gov/srtm/), [USGS GMTED2010](https://www.usgs.gov/coastal-changes-and-impacts/gmted2010), [USGS HYDRO1K](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-hydro1k) based on 1996 GTOPO30, [HydroLAKES](https://www.hydrosheds.org/products/hydrolakes), and [USCB TIGER/Line](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html).

Tools used include [QGIS](https://www.qgis.org/), [GDAL](https://gdal.org/), [GRASSGIS](https://grass.osgeo.org/),  [TouchTerrain](https://touchterrain.geol.iastate.edu/), [Anaconda](https://www.anaconda.com/), [GeoPandas](https://geopandas.org/en/stable/), [Matplotlib](https://matplotlib.org/), [Blender](https://www.blender.org/).
Please attribute open data and support FOSS software.

Tags
topography dual usa hydrography usaofplastic transparent topographic hydrographic rivers lakes streams mountains forests canyons valleys wall map cartography gis dem