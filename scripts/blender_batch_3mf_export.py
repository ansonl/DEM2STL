# 3D region model 3MF exporter
# Created by Anson Liu 2023
#
# License: AGPL v3
#
# This script automates the 3MF export of objects named in the below format. 
# Format: Abbreviation-PrintType-(land-elevation|hydrography|)-Style-pPartNumber
#   Abbreviation : Region abbreviation
#   PrintType (export) : single or dual [extrusion]
#   land-elevation and hydrography are checked if dual PrintType
#   Style : Special style e.g. transparent
#   pPartNumber: p followed by the partNumber if objects are part of a multi-piece multi-print model. Use 0 if not in a multi-piece model.

import os, re, bpy

regionsTopDir = 'K:/USAofPlasticv1/release_250m_v1/'

excludeList = ['AL','CO','ID','OR','MA','CA','FL','CT','WA']

allFiles = os.listdir(regionsTopDir)

def get_dir_size(path='.'):
  total = 0
  with os.scandir(path) as it:
    for entry in it:
      if entry.is_file():
        total += entry.stat().st_size
      elif entry.is_dir():
        total += get_dir_size(entry.path)
  return total

allFiles.sort(key=lambda f: get_dir_size(regionsTopDir+f), reverse=False)

regionList = allFiles

#regionList = ['XX']

def importSTL(abbr, printType, style):
  bpy.ops.import_mesh.stl(filepath=f'K:/USAofPlasticv1/release_250m_v1/{abbr}/{abbr}-{printType}{"-land-elevation" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}.STL')

  # import second model if dual PrintType
  if printType == "dual":
    bpy.ops.import_mesh.stl(filepath=f'K:/USAofPlasticv1/release_250m_v1/{abbr}/{abbr}-{printType}{"-hydrography" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}.STL')

def export3MF(abbr, printType, style, partNum):
  bpy.ops.object.select_all(action='DESELECT')

  for o in bpy.data.objects:
    # Check for given object names
    if re.search(f'{abbr}-{printType}{"-(?:land-elevation|hydrography)" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}{f"-p{partNum}" if partNum > 0 else ""}', o.name) is not None:
      o.select_set(True)

  # export objects
  if len(bpy.context.selected_objects) > 0:
    bpy.ops.export_mesh.threemf(filepath=f'K:/USAofPlasticv1/release_250m_v1/{abbr}/{abbr}-{printType}{"-" if len(style) > 0 else ""}{style}{f"-p{partNum}" if partNum > 0 else ""}.3mf', use_selection=True)

for rAbbr in regionList:
  # Skip if region is in exclude list
  if rAbbr in excludeList:
    continue

  # Import and export the different generated models
  importSTL(rAbbr, 'single', '')
  export3MF(rAbbr, 'single', '', 0)
  bpy.ops.object.delete() # delete the object afterwards to reduce unused memory usage

  importSTL(rAbbr, 'dual', '')
  export3MF(rAbbr, 'dual', '', 0)
  bpy.ops.object.delete()

  importSTL(rAbbr, 'dual', 'transparent')
  export3MF(rAbbr, 'dual', 'transparent', 0)
  bpy.ops.object.delete()

  # Export cut models (optional)
  export3MF(rAbbr, 'dual', 'transparent', 1)
  export3MF(rAbbr, 'dual', 'transparent', 2)
  export3MF(rAbbr, 'dual', 'transparent', 3)
  export3MF(rAbbr, 'dual', 'transparent', 4)