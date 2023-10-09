import bpy
import os
import sys
import time

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

if len(argv) < 2:
  print('need import file path(s) and export file path after -- INPUT1 INPUT2 ... EXPORT')

exportPath = ''

# Delete any existing objects
for o in bpy.data.objects:
  o.select_set(True)
bpy.ops.object.delete()

# Import each object in path
for i in argv:
  #last string in path is export path
  if i == argv[-1]:
    exportPath = i
  print(f'Importing {i}')
  bpy.ops.import_mesh.stl(filepath=i)
  print(f'Imported')

# Select all objects and export
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
  o.select_set(True)

print(f'Exporting all objects to {exportPath}')
startExportTime = time.monotonic()
bpy.ops.export_mesh.threemf(filepath=exportPath, use_selection=True)
print(f'Exported in {time.monotonic()-startExportTime}s')