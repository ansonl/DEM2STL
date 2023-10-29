# REGION_NAME (REGION_ABBR) Topographic Relief Map with Rivers and Coastal Waters

REGION_NAME mountains, coastlines, streams, and lakes in a dual or single color topographic and hydrographic map! All topographic states in the [USA of Plastic](https://www.printables.com/@ansonl/collections/714909) collection are at 1:2500000 scale and interlock with each other similar to a puzzle.

*[Download More 3D Printable Maps](https://ansonliu.com/maps/)*

*[Model and Map Specifications](https://ansonliu.com/maps/specifications/)*

# Recommended 3D Model Files to Print ↓ See 🌟 or ⭐ ↓

- REGION_ABBR-sqrt-dual.3mf 🌟 (Dual extrusion only ⚠️)
- REGION_ABBR-sqrt-single.3mf ⭐ (Single/Dual extrusion OK)

*Recommended to download only the model file name you need for faster download and less storage usage.*

![3D Map Variants](https://media.printables.com/media/prints/520841/images/4983945_1fdfa216-46f8-4da0-b22a-75d123423348_fba5a591-0e79-4da4-8628-35425e1dbed3/thumbs/inside/1600x1200/png/map-variants.webp)

### Model Filename Chart

```
STATE-ESCALING-EXTRUDER-STYLE-REVISION-PIECE##.3mf
     │                       │
     └────────VARIANT────────┘
```

| Definition | Meaning |
| ---- | ---- |
| `STATE` | State Abbreviation |
| `ESCALING` | Linear or Square Root (sqrt) elevation scaling. |
| `EXTRUDER` | Dual or Single color (extrusion) model |
| `STYLE`* *(optional)* | Model special style or subregion. `STYLE` is only present when the model file is a special style or the model is exclusive to a special subregion. |
| `REVISION` | Revision number. See [release notes](https://ansonliu.com/maps/release-notes/) for the latest improvements. |
| `PIECE##`† *(optional)* | Interlocking pre-cut piece ## sized for 180 mm x 180 mm bed. |

**Default `STYLE` is water features model located over submerged low lying lands. This submerged land may be visible when water layers are printed with a transparent filament. Default style minimizes usage of secondary (water) filament color. `transparent` style has water model features that extend all the way through the land for maximum light transmission when used with glow and transparent filaments.*

†*If multi-part files are not present, I have not created interlocking models for this state yet. Follow me and comment with your request to get future additions and updates.*

The models are in 3MF format which is like STL but better. 3MF has smaller file size and can store separate land and water objects that are aligned for easy dual color prints. 3MF is supported in Cura, PrusaSlicer, and other 3D slicers.

# Recommended print settings

Print the model flat. You can do a manual color change mid print to get interesting color transitions at higher elevations. Printers without multi-material capability should print the `*-single.3mf` models.

Show off streams, lakes, and coastlines with filament that is glow-in-the-dark or translucent — or simply use a different color from the base!

**Download the optimized Cura print settings profile for topo maps [HERE](https://www.printables.com/model/529276-contiguous-usa-lower-48-topographic-map-with-hydro).**

You can scale the model up or down as needed to fit your printer size, the final map's scale will just be scaled accordingly. *E.g. 200% scale on a previous scale of **0.4mm:1000m** results in **0.4mm:500m***

*If you rotate or scale models to fit your printer in Cura, merging objects `(Ctrl+Alt+G)` beforehand will help keep the dual color print objects aligned.*

Printing this will test your 3D printer's XY precision, Z-axis stability, retraction, cooling, and oozing!

| Slicer Setting | Recommended Value for 0.4 mm nozzle |
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

**Need a special location/map modeled and printed as a showpiece or gift?** [Contact me](mailto:maps@ansonliu.com) *([maps@ansonliu.com](mailto:maps@ansonliu.com))* for design and production services to bring your idea to life!

### Credits

USAofPlastic topographic map project uses data from [NASA SRTM V3.0](https://www2.jpl.nasa.gov/srtm/), [USGS GMTED2010](https://www.usgs.gov/coastal-changes-and-impacts/gmted2010), [USGS HYDRO1K](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-hydro1k) based on 1996 GTOPO30, [HydroLAKES](https://www.hydrosheds.org/products/hydrolakes), and [USCB TIGER/Line](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html).

Tools used include [QGIS](https://www.qgis.org/), [GDAL](https://gdal.org/), [GRASSGIS](https://grass.osgeo.org/),  [TouchTerrain](https://touchterrain.geol.iastate.edu/), [Anaconda](https://www.anaconda.com/), [GeoPandas](https://geopandas.org/en/stable/), [Matplotlib](https://matplotlib.org/), [Blender](https://www.blender.org/).
Please support open data and FOSS software.

Tags
topography dual usa hydrography usaofplastic transparent topographic hydrographic rivers lakes streams mountains forests canyons valleys wall map cartography gis dem