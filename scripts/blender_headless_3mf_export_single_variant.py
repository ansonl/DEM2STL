import bpy
import re
import os
import time

# cd 'C:\Program Files\Blender Foundation\Blender 3.5\'
# ./blender.exe -b --python C:\Users\ansonl\development\dem-to-stl-workflow\scripts\headless_blender_3mf_export_single_variant.py

regionsTopDir = 'K:/USAofPlasticv1/release_250m_v1/'
regionsTopDir = 'C:/Users/ansonl/development/dem-to-stl-workflow/state_stls/usa-individual-states-linear/250/'

excludeList = []


def importSTL(abbr, printType, style):
    bpy.ops.import_mesh.stl(
        filepath=f'{regionsTopDir}{abbr}/{abbr}-{printType}{"-land-elevation" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}.STL', global_scale=0.001)

    # import second model if dual PrintType
    if printType == "dual":
        bpy.ops.import_mesh.stl(
            filepath=f'{regionsTopDir}{abbr}/{abbr}-{printType}{"-hydrography" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}.STL', global_scale=0.001)


def export3MF(abbr, printType, style, partNum):
    bpy.ops.object.select_all(action='DESELECT')

    for o in bpy.data.objects:
        # Check for given object names
        if re.search(f'{abbr}-{printType}{"-(?:land-elevation|hydrography)" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}{f"-p{partNum}" if partNum > 0 else ""}', o.name) is not None:
            o.select_set(True)

    # export objects
    if len(bpy.context.selected_objects) > 0:
        bpy.ops.export_mesh.threemf(
            filepath=f'{regionsTopDir}{abbr}/{abbr}-{printType}{"-" if len(style) > 0 else ""}{style}{f"-p{partNum}" if partNum > 0 else ""}.3mf', use_selection=True)


def processEntry(rAbbr):
    
    print(f'Starting {rAbbr} single')

    importSTL(rAbbr, 'single-linear-scale-v2', '')
    variantProcessStartTime = time.monotonic()
    export3MF(rAbbr, 'single-linear-scale-v2', '', 0)
    bpy.ops.object.delete()  # delete the object afterwards to reduce unused memory usage

    """
    print('Starting dual')

    importSTL(rAbbr, 'dual', '')
    export3MF(rAbbr, 'dual', '', 0)
    bpy.ops.object.delete()

    print('Starting dual transparent')

    importSTL(rAbbr, 'dual', 'transparent')
    export3MF(rAbbr, 'dual', 'transparent', 0)
    bpy.ops.object.delete()
    """

    print(f'{rAbbr} export took {time.monotonic()-variantProcessStartTime}s')
    print('Finished')


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
                if exclude3MF and entry.name.endswith('single-linear-scale-v2.3mf'):
                    excludeList.append(path[path.rfind('/')+1:])
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


regionList.sort(key=lambda f: get_dir_size(regionsTopDir+f), reverse=False)

for rAbbr in regionList:
    if rAbbr in excludeList:
        continue
    processEntry(rAbbr)
