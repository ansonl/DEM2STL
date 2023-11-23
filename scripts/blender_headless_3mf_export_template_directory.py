import bpy
import re
import os
import sys
import time

# usage syntax

# Auto mode
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- autoTemplateDir DIR_WITH_ABBR_FOLDERS MAP-E-SCALE-LABEL VERSION-STRING #PRIXXXFF #SECXXXFF

# Manual mode
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- manual INPUT1 #PRIXXXFF(optional) INPUT2 #SECXXXFF(optional) ... EXPORT

# colors for printablescom render
# all colors shifted orange in printables preview
# 2AE3FF cyan shows as blue in printables
# FFE066 yellow
# C5F178 lime

# cd 'C:\Program Files\Blender Foundation\Blender 3.5\'
# ./blender.exe -b --python C:\Users\ansonl\development\dem-to-stl-workflow\scripts\blender_headless_3mf_export_template_directory.py -- C:\Users\ansonl\Downloads\share\staging\state_stls\test\ test v1 `#C5F178FF `#2AE3FFFF

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
regionsTopDir, scaleTitle, versionTitle, hexColors = '', '', '', []

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
        hexColors.append(tuple(float(int(argv[4].lstrip('#')[i:i+2], 16))/255 for i in (0, 2, 4, 6)))
    if len(argv) > 5:
        hexColors.append(tuple(float(int(argv[5].lstrip('#')[i:i+2], 16))/255 for i in (0, 2, 4, 6)))

excludeList = []

# setup scene for 3d print export
def setupScene():
    # Delete any existing objects
    for o in bpy.data.objects:
      o.select_set(True)
    bpy.ops.object.delete()

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

    #set scene from m to mm
    bpy.data.scenes["Scene"].unit_settings.scale_length = 0.001

def importSTL(path, addMaterialFromIndex):
    print(f'Importing {path}')
    bpy.ops.import_mesh.stl(
        filepath=path)
    if addMaterialFromIndex != -1 and len(materials) > addMaterialFromIndex:
      bpy.context.selected_objects[0].data.materials.append(materials[addMaterialFromIndex])

def export3MF(path):
    print(f'Exporting {path}')
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

def export3MFTemplate(abbr, scale, printType, style, version, partNum):
    bpy.ops.object.select_all(action='DESELECT')

    for o in bpy.data.objects:
        # Check for given object names
        if re.search(f'{abbr}-{printType}{"-(?:land-elevation|hydrography)" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}{f"-p{partNum}" if partNum > 0 else ""}', o.name) is not None:
            o.select_set(True)

    exportPath = f'{regionsTopDir}{abbr}/{abbr}{"-" if len(scale) > 0 else ""}{scale}-{printType}{"-" if len(style) > 0 else ""}{style}{"-" if len(version) > 0 else ""}{version}{f"-p{partNum}" if partNum > 0 else ""}.3mf'
    print(f'Exporting {exportPath}')

    # export objects
    if len(bpy.context.selected_objects) > 0:
        export3MF(exportPath)

def processEntry(rAbbr, scale, version):
    print(f'Starting {rAbbr} single')

    importSTLTemplate(rAbbr, 'single', '')
    export3MFTemplate(rAbbr, scale, 'single', '', version, 0)
    bpy.ops.object.delete()  # delete the object afterwards to reduce unused memory usage

    print(f'Starting {rAbbr} dual')

    importSTLTemplate(rAbbr, 'dual', '')
    export3MFTemplate(rAbbr, scale, 'dual', '', version, 0)
    bpy.ops.object.delete()

    print(f'Starting {rAbbr} dual transparent')

    importSTLTemplate(rAbbr, 'dual', 'transparent')
    export3MFTemplate(rAbbr, scale, 'dual', 'transparent', version, 0)
    bpy.ops.object.delete()

    print(f'Finished {rAbbr}')

setupScene()

if mode == MODE_MANUAL:
    for x in range(len(manualImportFilePaths)):
        importSTL(manualImportFilePaths[x][0], manualImportFilePaths[x][1])
    export3MF(manualExportFilePath)
    print(f'Finished with manual mode 3MF export')

if mode == MODE_AUTOTEMPLATEDIR:
    os.chdir(regionsTopDir)
    regionList = os.listdir(regionsTopDir)
    excludeList = []

    def get_dir_size(path='.', exclude3MF=True):
        total = 0
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    if entry.name.endswith('.stl'):
                        total += entry.stat().st_size
                    if exclude3MF and entry.name.endswith('transparent.3mf'):
                        excludeList.append(path[path.rfind('/')+1:])
                elif entry.is_dir():
                    total += get_dir_size(entry.path)
        return total


    regionList.sort(key=lambda f: get_dir_size(regionsTopDir+f), reverse=False)

    for rAbbr in regionList:
        """
        if rAbbr in excludeList:
            continue
        """
        processEntry(rAbbr, scaleTitle, versionTitle)
