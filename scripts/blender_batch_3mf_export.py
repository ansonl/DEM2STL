# 3D region model 3MF exporter
# Created by Anson Liu 2023
#
# License: AGPL v3
#
# This script automates the 3MF export of objects named in the below format. 
# Format: Abbreviation-PrintType-(land-elevation|hydrography|)-Style-pPartNumber
#   Abbreviation : Region abbreviation
#   PrintType : single or dual [extrusion]
#   land-elevation and hydrography are checked if dual PrintType
#   Style : Special style e.g. transparent
#   pPartNumber: p followed by the partNumber if objects are part of a multi-piece multi-print model. Use 0 if not in a multi-piece model.

import re, bpy

regionAbbr = 'XX'

def export3MF(abbr, printType, style, partNum):
  bpy.ops.object.select_all(action='DESELECT')

  for o in bpy.data.objects:
    # Check for given object names
    if re.search(f'{abbr}-{printType}{"-(?:land-elevation|hydrography)" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}{f"-p{partNum}" if partNum > 0 else ""}', o.name) is not None:
      o.select_set(True)

  # export objects
  if len(bpy.context.selected_objects) > 0:
    bpy.ops.export_mesh.threemf(filepath=f'K:/USAofPlasticv1/release_250m_v1/{abbr}/{abbr}-{printType}{"-" if len(style) > 0 else ""}{style}{f"-p{partNum}" if partNum > 0 else ""}.3mf', use_selection=True)

# Export generated models
export3MF(regionAbbr, 'single', '', 0)
export3MF(regionAbbr, 'dual', '', 0)
export3MF(regionAbbr, 'dual', 'transparent', 0)

# Export cut models
export3MF(regionAbbr, 'dual', 'transparent', 1)
export3MF(regionAbbr, 'dual', 'transparent', 2)
export3MF(regionAbbr, 'dual', 'transparent', 3)
export3MF(regionAbbr, 'dual', 'transparent', 4)