import bpy
import re
import os
import sys
import time

# usage syntax

# Auto mode
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- autoTemplateDir DIR_WITH_ABBR_FOLDERS MAP-E-SCALE-LABEL VERSION-STRING NEW-VERSION-STRING #PRIXXXFF #SECXXXFF

# Manual mode
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- manual INPUT1 #PRIXXXFF(optional) INPUT2 #SECXXXFF(optional) ... EXPORT

# colors for printablescom render
# all colors shifted orange in printables preview
# 2AE3FF cyan shows as blue in printables
# FFE066 yellow
# C5F178 lime

# Start-Transcript decimate.log

# cd 'C:\Program Files\Blender Foundation\Blender 3.5\'
# ./blender.exe -b --python C:\Users\ansonl\development\dem-to-stl-workflow\scripts\blender_headless_3mf_import_decimate_bottom_export_template_directory.py -- autoTemplateDir K:\USAofPlastic\USAofPlasticv2test\ linear v2 v2 `#C5F178FF `#2AE3FFFF
# ./blender.exe -b --python C:\Users\ansonl\development\dem-to-stl-workflow\scripts\blender_headless_3mf_import_decimate_bottom_export_template_directory.py -- autoTemplateDir K:\USAofPlastic\USAofPlasticv2test\ sqrt v1 v2 `#C5F178FF `#2AE3FFFF

# Stop-Transcript

#./blender.exe -b --python  C:\Users\ansonl\development\dem-to-stl-workflow\scripts\blender_headless_3mf_import_decimate_bottom_export_template_directory.py -- manual K:\USAofPlastic\USAofPlasticv2test\DC\DC-linear-dual-v2.3mf K:\USAofPlastic\USAofPlasticv2test\DC\DC-linear-dual-v2-decim.3mf

#./blender.exe -b --python  C:\Users\ansonl\development\dem-to-stl-workflow\scripts\blender_headless_3mf_import_decimate_bottom_export_template_directory.py -- manual K:\USAofPlastic\USAofPlasticv2test\DC\DC-linear-single-v2.3mf K:\USAofPlastic\USAofPlasticv2test\DC\DC-linear-single-v2.3mf

# server
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/usa-individual-states-linear/250/ linear v2
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/usa-individual-states-sqrt/250/ sqrt v1

# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/ak-na-conformal-conic-linear/250/ linear v1
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/ak-na-conformal-conic-sqrt/250/ sqrt v1

# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- autoTemplateDir ~/data/state_stls/cn-asia-conformal-conic-linear/1000/ linear v1

# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- manual ~/data/state_stls/cn-asia-conformal-conic-linear/1000/CN/CN-dual-land-elevation-transparent.stl ~/data/state_stls/cn-asia-conformal-conic-linear/1000/CN/CN-dual-hydrography-transparent.stl ~/data/state_stls/cn-asia-conformal-conic-linear/1000/CN/CN-dual-transparent.3mf

# cd 'C:\Program Files\Blender Foundation\Blender 3.5\'
# ./blender.exe -b -noaudio --python C:\Users\ansonl\development\dem-to-stl-workflow\scripts\blender_headless_3mf_export_template_directory.py -- manual ~/data/state_stls/cn-asia-conformal-conic-linear/1000/CN/CN-dual-land-elevation-transparent.stl ~/data/state_stls/cn-asia-conformal-conic-linear/1000/CN/CN-dual-hydrography-transparent.stl ~/data/state_stls/cn-asia-conformal-conic-linear/1000/CN/CN-dual-transparent.3mf


argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

MODE_UNKNOWN = 0
MODE_MANUAL = 1 # manual
MODE_AUTOTEMPLATEDIR = 2 # autoTemplateDir

#args storage
mode = MODE_UNKNOWN
regionsTopDir, scaleTitle, versionTitle, newVersionTitle, hexColors = '', '', '', '', []

manualImportFilePaths, manualExportFilePath = [], ''

if len(argv) < 2:
    print('not enough args')
if len(argv) > 0:
    if argv[0] == 'manual':
        mode = MODE_MANUAL
    elif argv[0] == 'autoTemplateDir':
        mode = MODE_AUTOTEMPLATEDIR
    else:
        print('invalid mode entered')

if mode == MODE_MANUAL:
    k = 1
    while k < len(argv):
        importFileAndColor = [argv[k], -1]
        # look for color code as next arg after filename
        if k < len(argv) - 2 and argv[k+1][0] == '#':
            hexColors.append(tuple(float(int(argv[i+1].lstrip('#')[k:k+2], 16))/255 for i in (0, 2, 4, 6)))
            importFileAndColor[1] = len(hexColors)-1
            k += 1 #skip next index which is the color for this model
        
        # last arg is export filename
        if k == len(argv) - 1:
            manualExportFilePath = argv[k]
            break
        manualImportFilePaths.append(importFileAndColor)
        
        k+=1

if mode == MODE_AUTOTEMPLATEDIR:
    if len(argv) > 1:
        regionsTopDir = argv[1]
    if len(argv) > 2:
        scaleTitle = argv[2]
    if len(argv) > 3:
        versionTitle = argv[3]
    if len(argv) > 4:
        newVersionTitle = argv[4]
    if len(argv) > 5:
        hexColors.append(tuple(float(int(argv[5].lstrip('#')[i:i+2], 16))/255 for i in (0, 2, 4, 6)))
    if len(argv) > 6:
        hexColors.append(tuple(float(int(argv[6].lstrip('#')[i:i+2], 16))/255 for i in (0, 2, 4, 6)))

excludeList = []

def createMaterials():
    global materials
    # create materials if colors specified
    materials = []
    if len(hexColors) > 0:
        # Delete existing materials
        for m in bpy.data.materials:
            bpy.data.materials.remove(m)    
        
        # set colors
        materials.append(bpy.data.materials.new("Primary"))
        materials[0].use_nodes = True
        materials[0].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = hexColors[0]
        materials.append(bpy.data.materials.new("Secondary"))
        materials[1].use_nodes = True
        materials[1].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = hexColors[1]
        print("Using colors", hexColors[0], hexColors[1])
    else:
        print("No primary and secondary color provided")

# setup scene for 3d print export
def setupScene():
    # Delete any existing objects
    for o in bpy.data.objects:
        o.select_set(True)
    bpy.ops.object.delete()

    #set scene from m to mm
    bpy.data.scenes["Scene"].unit_settings.scale_length = 0.001

def importSTL(path, addMaterialFromIndex):
    print(f'Importing {path}')
    bpy.ops.import_mesh.stl(
        filepath=path)
    if addMaterialFromIndex != -1 and len(materials) > addMaterialFromIndex:
      bpy.context.selected_objects[0].data.materials.append(materials[addMaterialFromIndex])

def import3MF(path, addMaterialFromIndex, use_color_group):
    print(f'Importing {path}')
    startTime = time.monotonic()
    bpy.ops.import_mesh.threemf(
        filepath=path, use_color_group=use_color_group)
    if addMaterialFromIndex != -1 and len(materials) > addMaterialFromIndex:
      for o in bpy.context.selected_objects:
          if o.data and len(o.data.materials) == 0:
            print(f'{o.name} has no material assigned so it is assigned material {materials[addMaterialFromIndex]}')
            o.data.materials.append(materials[addMaterialFromIndex])
            addMaterialFromIndex += 1
    print(f'Imported in {time.monotonic()-startTime}s')

def export3MF(path):
    print(f'Exporting {len(bpy.data.objects)} objects to to {path}')
    startExportTime = time.monotonic()
    bpy.ops.export_mesh.threemf(
        filepath=path, use_selection=True, coordinate_precision=6, use_color_group=True)
    print(f'Exported in {time.monotonic()-startExportTime}s')

# import STL with template filename format
def importSTLTemplate(abbr, printType, style):
    importPath = f'{regionsTopDir}{abbr}/{abbr}-{printType}{"-land-elevation" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}.stl'
    print(f'Importing {importPath}')
    importSTL(importPath, 0)

    # import second model if dual PrintType
    if printType == "dual":
        secondImportPath = f'{regionsTopDir}{abbr}/{abbr}-{printType}{"-hydrography" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}.stl'
        print(f'Importing {secondImportPath}')
        importSTL(secondImportPath, 1)

# import 3MF with template filename format
def import3MFTemplate(abbr, scale, printType, style, version):
    importPath = f'{regionsTopDir}{abbr}/{abbr}-{scale}-{printType}{"-" if len(style) > 0 else ""}{style}-{version}.3mf'
    import3MF(importPath, addMaterialFromIndex=0, use_color_group=True)

def export3MFTemplate(abbr, scale, printType, style, version, partNum):
    bpy.ops.object.select_all(action='DESELECT')

    for o in bpy.data.objects:
        # Check for given object names
        if re.search(f'{abbr}-{printType}{"-(?:land-elevation|hydrography)" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}{f"-p{partNum}" if partNum > 0 else ""}', o.name) is not None:
            o.select_set(True)

    if len(bpy.context.selected_objects) == 0:
          print(f'No object names matched land-elevation or hydrography so selecting all objects for export.')
          for o in bpy.data.objects:
              o.select_set(True)

    exportPath = f'{regionsTopDir}{abbr}/{abbr}{"-" if len(scale) > 0 else ""}{scale}-{printType}{"-" if len(style) > 0 else ""}{style}{"-" if len(version) > 0 else ""}{version}{f"-p{partNum}" if partNum > 0 else ""}.3mf'
    print(f'Exporting {exportPath}')

    # export objects
    if len(bpy.context.selected_objects) > 0:
        export3MF(exportPath)


# decimate bottom inner vertices to 1%
def decimateBottomInnerVertices(targetObject):
  if targetObject.data is None:
      print(f'{targetObject.name} data is none. Skipping decimating the object.')
      return

  bpy.context.view_layer.objects.active = targetObject

  originalVertexCount = 0
  originalVertexCount += len(targetObject.data.vertices)
      
  print(f'{targetObject.name} - Original vertex count: {originalVertexCount}')

  decimateStartTime = time.monotonic()

  for e in [targetObject.data.vertices, targetObject.data.polygons, targetObject.data.edges]:
      e.foreach_set("select", (False,)*len(e))

  for v in targetObject.data.vertices:
    v.select = v.co.z <= 0
    
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_mode(type="VERT")
  bpy.ops.mesh.select_less()
    
  bpy.ops.object.vertex_group_assign_new()
  targetObject.vertex_groups[0].name = 'bottom-inner'

  print(f'Selection took {time.monotonic()-decimateStartTime}s')

  bpy.ops.object.mode_set(mode='OBJECT')

  bpy.ops.object.modifier_add(type='DECIMATE')
  bpy.context.object.modifiers["Decimate"].vertex_group='bottom-inner'
  bpy.context.object.modifiers["Decimate"].ratio=0.01
  bpy.ops.object.mode_set(mode='OBJECT')
  bpy.ops.object.modifier_apply(modifier='Decimate')

  print(f'Decimate Bottom & Selection took {time.monotonic()-decimateStartTime}s')

  endVertexCount = len(targetObject.data.vertices)

  print(f'{targetObject.name} - Decimated end vertex count: {endVertexCount} - {endVertexCount/originalVertexCount*100}% of original vertex count')

def processEntry(rAbbr, scale, version, newVersion):
    print(f'Starting {rAbbr} single')

    createMaterials()
    import3MFTemplate(rAbbr, scale=scale, printType='single', style='', version=version)
    for o in bpy.data.objects:
      decimateBottomInnerVertices(o)
    export3MFTemplate(rAbbr, scale, 'single', '', newVersion, 0)
    bpy.ops.object.delete()  # delete the object afterwards to reduce unused memory usage
    bpy.ops.outliner.orphans_purge() # purge remaining mesh left behind by object, this also deletes materials
    print(f'Remaining objects count {len(bpy.data.objects)}')

    print(f'Starting {rAbbr} dual')

    createMaterials()
    import3MFTemplate(rAbbr, scale=scale, printType='dual', style='', version=version)
    for o in bpy.data.objects:
      decimateBottomInnerVertices(o)
    export3MFTemplate(rAbbr, scale, 'dual', '', newVersion, 0)
    bpy.ops.object.delete()
    bpy.ops.outliner.orphans_purge() # purge remaining mesh left behind by object, this also deletes materials
    print(f'Remaining objects count {len(bpy.data.objects)}')

    print(f'Starting {rAbbr} dual transparent')

    createMaterials()
    import3MFTemplate(rAbbr, scale=scale, printType='dual', style='transparent', version=version)
    for o in bpy.data.objects:
      decimateBottomInnerVertices(o)
    export3MFTemplate(rAbbr, scale, 'dual', 'transparent', newVersion, 0)
    bpy.ops.object.delete()
    bpy.ops.outliner.orphans_purge() # purge remaining mesh left behind by object, this also deletes materials
    print(f'Remaining objects count {len(bpy.data.objects)}')

    print(f'Finished {rAbbr}')

setupScene()

if mode == MODE_MANUAL:
    for x in range(len(manualImportFilePaths)):
        import3MF(manualImportFilePaths[x][0], addMaterialFromIndex=0, use_color_group=True)
    for o in bpy.data.objects:
      decimateBottomInnerVertices(o)
    for o in bpy.data.objects:
        o.select_set(True)
    export3MF(manualExportFilePath)
    print(f'Finished with manual mode 3MF export')

if mode == MODE_AUTOTEMPLATEDIR:
    os.chdir(regionsTopDir)
    regionList = os.listdir(regionsTopDir)
    excludeList = []

    def get_dir_size(path='.', exclude3MF=False):
        total = 0
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    if entry.name.endswith('.3mf'):
                        total += entry.stat().st_size
                    if exclude3MF and entry.name.endswith('transparent.3mf'):
                        excludeList.append(path[path.rfind('/')+1:])
                elif entry.is_dir():
                    total += get_dir_size(entry.path)
        return total


    regionList.sort(key=lambda f: get_dir_size(regionsTopDir+f), reverse=False)

    print(regionList)

    for rAbbr in regionList:
        
        if rAbbr in excludeList:
            continue
        
        processEntry(rAbbr, scaleTitle, versionTitle, newVersionTitle)
