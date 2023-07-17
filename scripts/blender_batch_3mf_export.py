# 3D region model 3MF exporter
# Created by Anson Liu 2023

# License: AGPL v3

import re, bpy

def export3MF(abbr, printType, style, partNum):
  bpy.ops.object.select_all(action='DESELECT')

  for o in bpy.data.objects:
    # Check for given object names
    if re.search(f'{abbr}-{printType}{"-(?:land-elevation|hydrography)" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}{"-p" if partNum > 0 else ""}{partNum}', o.name) is not None:
      o.select_set(True)

  # export objects
  bpy.ops.export_mesh.threemf(filepath=f'K:/USAofPlasticv1/release_250m_v1/{abbr}/{abbr}-{printType}{"-" if len(style) > 0 else ""}{style}{"-p" if partNum > 0 else ""}{partNum}.3mf', use_selection=True)
  
regionAbbr = 'RI'

# Export generated models
export3MF(regionAbbr, 'single', '', 0)
export3MF(regionAbbr, 'dual', '', 0)
export3MF(regionAbbr, 'dual', 'transparent', 0)

# Export cut models
export3MF(regionAbbr, 'dual', 'transparent', 1)
export3MF(regionAbbr, 'dual', 'transparent', 2)
export3MF(regionAbbr, 'dual', 'transparent', 3)
export3MF(regionAbbr, 'dual', 'transparent', 4)