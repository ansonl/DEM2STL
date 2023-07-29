import bpy
import re

regionsTopDir = 'K:/USAofPlasticv1/release_250m_v1/'

excludeList = []

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

rAbbr = 'TX'

#print('Starting single')

#importSTL(rAbbr, 'single', '')
#export3MF(rAbbr, 'single', '', 0)
#bpy.ops.object.delete() # delete the object afterwards to reduce unused memory usage

print('Starting dual')

importSTL(rAbbr, 'dual', '')
export3MF(rAbbr, 'dual', '', 0)
bpy.ops.object.delete()

print('Starting dual transparent')

importSTL(rAbbr, 'dual', 'transparent')
export3MF(rAbbr, 'dual', 'transparent', 0)
bpy.ops.object.delete()

print('Finished')