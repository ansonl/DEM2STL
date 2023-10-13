import bpy
import re
import os
import sys
import time

# cd 'C:\Program Files\Blender Foundation\Blender 3.5\'
# ./blender.exe -b --python --- C:\Users\ansonl\development\dem-to-stl-workflow\scripts\headless_blender_3mf_export.py DIR_WITH_ABBR_FOLDERS

# server
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/usa-individual-states-linear/250/ linear v2
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/usa-individual-states-sqrt/250/ sqrt v1

# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/ak-na-conformal-conic-linear/250/ linear v1
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/ak-na-conformal-conic-sqrt/250/ sqrt v1


# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/cn-asia-conformal-conic-linear/1000/ linear v1
# ~/blender-3.4.1-linux-x64/blender -b -noaudio --python ./blender_headless_3mf_export_template_directory.py -- ~/data/state_stls/cn-asia-conformal-conic-sqrt/1000/ sqrt v1

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

regionsTopDir, scaleTitle, versionTitle = '', '', ''

if len(argv) < 2:
    print('not enough args')
if len(argv) > 0:
    regionsTopDir = argv[0]
if len(argv) > 1:
    scaleTitle = argv[1]
if len(argv) > 2:
    versionTitle = argv[2]

excludeList = []

#set scene from m to mm
bpy.data.scenes["Scene"].unit_settings.scale_length = 0.001

def importSTL(abbr, printType, style):
    importPath = f'{regionsTopDir}{abbr}/{abbr}-{printType}{"-land-elevation" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}.stl'
    print(f'Importing {importPath}')

    bpy.ops.import_mesh.stl(
        filepath=importPath)

    # import second model if dual PrintType
    if printType == "dual":
        secondImportPath = f'{regionsTopDir}{abbr}/{abbr}-{printType}{"-hydrography" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}.stl'
        print(f'Importing {secondImportPath}')
        bpy.ops.import_mesh.stl(
            filepath=secondImportPath)


def export3MF(abbr, scale, printType, style, version, partNum):
    bpy.ops.object.select_all(action='DESELECT')

    for o in bpy.data.objects:
        # Check for given object names
        if re.search(f'{abbr}-{printType}{"-(?:land-elevation|hydrography)" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}{f"-p{partNum}" if partNum > 0 else ""}', o.name) is not None:
            o.select_set(True)

    exportPath = f'{regionsTopDir}{abbr}/{abbr}{"-" if len(scale) > 0 else ""}{scale}-{printType}{"-" if len(style) > 0 else ""}{style}{"-" if len(version) > 0 else ""}{version}{f"-p{partNum}" if partNum > 0 else ""}.3mf'
    print(f'Exporting {exportPath}')

    # export objects
    if len(bpy.context.selected_objects) > 0:
        startExportTime = time.monotonic()
        bpy.ops.export_mesh.threemf(
            filepath=exportPath, use_selection=True, coordinate_precision=6)
        print(f'Exported in {time.monotonic()-startExportTime}s')


def processEntry(rAbbr, scale, version):
    print(f'Starting {rAbbr} single')

    importSTL(rAbbr, 'single', '')
    export3MF(rAbbr, scale, 'single', '', version, 0)
    bpy.ops.object.delete()  # delete the object afterwards to reduce unused memory usage

    print(f'Starting {rAbbr} dual')

    importSTL(rAbbr, 'dual', '')
    export3MF(rAbbr, scale, 'dual', '', version, 0)
    bpy.ops.object.delete()

    print(f'Starting {rAbbr} dual transparent')

    importSTL(rAbbr, 'dual', 'transparent')
    export3MF(rAbbr, scale, 'dual', 'transparent', version, 0)
    bpy.ops.object.delete()

    print(f'Finished {rAbbr}')


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
