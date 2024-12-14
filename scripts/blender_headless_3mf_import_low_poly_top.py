import bpy
import re
import os
import sys
import time

# usage syntax

# Auto mode
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_import_low_poly_top.py -- autoTemplateDir DIR_WITH_ABBR_FOLDERS MAP-E-SCALE-LABEL VERSION-STRING NEW-VERSION-STRING #PRIXXXFF #SECXXXFF

# Manual mode
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_import_low_poly_top.py -- manual INPUT1 #PRIXXXFF(optional) INPUT2 #SECXXXFF(optional) ... EXPORT

# colors for printablescom render
# all colors shifted orange in printables preview
# 2AE3FF cyan shows as blue in printables
# FFE066 yellow
# C5F178 lime

# Start-Transcript decimate.log

# cd 'C:\Program Files\Blender Foundation\Blender 3.5\'
# ./blender.exe -b --python C:\Users\ansonl\development\dem-to-stl-workflow\scripts\blender_headless_3mf_import_low_poly_top.py -- autoTemplateDir K:\USAofPlastic\USAofPlasticv2.2\ linear v2 v2 `#C5F178FF `#2AE3FFFF
# ./blender.exe -b --python C:\Users\ansonl\development\dem-to-stl-workflow\scripts\blender_headless_3mf_import_low_poly_top.py -- autoTemplateDir K:\USAofPlastic\USAofPlasticv2.2\ sqrt v2 v2 `#C5F178FF `#2AE3FFFF


#./blender.exe -b --python C:\Users\ansonl\development\dem-to-stl-workflow\scripts\blender_headless_3mf_import_low_poly_top.py -- manual K:\USAofPlastic\USAofPlasticv2.2\DE\DE-linear-dual-transparent-v2.3mf K:\USAofPlastic\USAofPlasticv2.2\DE\DE-linear-dual-transparent-v2-lowpoly.3mf

# Stop-Transcript

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

materials = []

def createMaterials():
    global materials
    materials = []
    # create materials if colors specified
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
def import3MFTemplate(abbr, scale, printType, style, version, use_color_group):
    importPath = f'{regionsTopDir}{abbr}/{abbr}-{scale}-{printType}{"-" if len(style) > 0 else ""}{style}-{version}.3mf'
    import3MF(importPath, addMaterialFromIndex=0, use_color_group=use_color_group)

def export3MFTemplate(abbr, scale, printType, style, version, postProcess, partNum):
    bpy.ops.object.select_all(action='DESELECT')

    for o in bpy.data.objects:
        o.select_set(True)

    exportPath = f'{regionsTopDir}{abbr}/{abbr}{"-" if len(scale) > 0 else ""}{scale}-{printType}{"-" if len(style) > 0 else ""}{style}{"-" if len(version) > 0 else ""}{version}{f"-{postProcess}" if postProcess else ""}{f"-p{partNum}" if partNum > 0 else ""}.3mf'
    print(f'Exporting {exportPath}')

    # export objects
    if len(bpy.context.selected_objects) > 0:
        export3MF(exportPath)

# merge top surface inner vertices to by 2mm
def mergeTopInnerVertices(targetObject):
    #desired_threshold_border = 0.001
    original_vertex_resolution = 0.0001 #0.1mm
    desired_threshold = 0.002 #2mm
    inset_steps = int(desired_threshold/original_vertex_resolution)

    scaleZ = 3

    modelBaseThicknessAtSeaLevel = 0.9
    sinkDownZ = modelBaseThicknessAtSeaLevel*(scaleZ-1)

    if targetObject.data is None:
        print(f'{targetObject.name} data is none. Skipping decimating the object.')
        return

    bpy.context.view_layer.objects.active = targetObject

    originalVertexCount = len(bpy.context.active_object.data.vertices)
        
    print(f'{bpy.context.active_object.name} - Original vertex count: {originalVertexCount}')

    variantProcessStartTime = time.monotonic()

    print(f'Starting low polyization of top surface')

    # low poly top surface inner
    # select inner land without outer border to merge
    for e in [bpy.context.active_object.data.vertices, bpy.context.active_object.data.polygons, bpy.context.active_object.data.edges]:
        e.foreach_set("select", (False,)*len(e))

    for v in bpy.context.active_object.data.vertices:
        v.select = v.co.z <= 0

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_more()

    for _ in range(inset_steps):
        bpy.ops.mesh.select_more()

    bpy.ops.mesh.select_all(action='INVERT')

    recalculated_threshold = desired_threshold / bpy.context.scene.unit_settings.scale_length

    bpy.ops.mesh.remove_doubles(threshold=recalculated_threshold, use_unselected=False)

    bpy.ops.object.mode_set(mode='OBJECT')

    # scale up all vertices Z by 300% and correct base level back to original base level
    for v in bpy.context.active_object.data.vertices:
        if v.co.z > 0:
            v.co.z *= scaleZ
            v.co.z -= sinkDownZ
            
    # print Status
    endVertexCount = len(bpy.context.active_object.data.vertices)

    print(f'{bpy.context.active_object.name} - End vertex count {endVertexCount} - {endVertexCount/originalVertexCount*100}% of original vertex count')        

    print(f'Low poly took {time.monotonic()-variantProcessStartTime}s')

def checkAndRepairNonSolid(targetObject):
    if targetObject.data is None:
        print(f'{targetObject.name} data is none. Skipping repair the object.')
        return
  
    bpy.context.view_layer.objects.active = targetObject
    
    print(f'Making object manifold')
    
    bpy.ops.mesh.print3d_clean_non_manifold()
    
    print(f'Finished object manifold')

def processEntry(rAbbr, scale, version, newVersion):
    print(f'Starting {rAbbr} single')

    createMaterials()
    import3MFTemplate(rAbbr, scale=scale, printType='single', style='', version=version, use_color_group=True)
    for o in bpy.data.objects:
        o.select_set(False)
        mergeTopInnerVertices(o)
        checkAndRepairNonSolid(o)
        o.select_set(False)
    export3MFTemplate(rAbbr, scale, 'single', '', newVersion, 'lowpoly', 0)
    bpy.ops.object.delete()  # delete the object afterwards to reduce unused memory usage
    bpy.ops.outliner.orphans_purge() # purge remaining mesh left behind by object, this also deletes materials
    print(f'Remaining objects count {len(bpy.data.objects)}')

    print(f'Starting {rAbbr} dual transparent')

    createMaterials()
    import3MFTemplate(rAbbr, scale=scale, printType='dual', style='transparent', version=version, use_color_group=True)
    for o in bpy.data.objects:
        o.select_set(False)
        mergeTopInnerVertices(o)
        checkAndRepairNonSolid(o)
        o.select_set(False)
    export3MFTemplate(rAbbr, scale, 'dual', 'transparent', newVersion, 'lowpoly', 0)
    bpy.ops.object.delete()
    bpy.ops.outliner.orphans_purge() # purge remaining mesh left behind by object, this also deletes materials
    print(f'Remaining objects count {len(bpy.data.objects)}')

    print(f'Finished {rAbbr}')

setupScene()

if mode == MODE_MANUAL:
    for x in range(len(manualImportFilePaths)):
        import3MF(manualImportFilePaths[x][0], addMaterialFromIndex=0, use_color_group=False)
    for o in bpy.data.objects:
        o.select_set(False)
        mergeTopInnerVertices(o)
        checkAndRepairNonSolid(o)
        o.select_set(False)
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
