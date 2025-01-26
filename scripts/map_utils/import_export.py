import bpy, time, os

from enum import Enum
from typing import List

class FileExtensions(Enum):
    UNKNOWN = "unknown"
    STL = ".stl"
    THREEMF = ".3mf"

def importSTL(path: str, material: bpy.types.Material):
    print(f'Importing STL {path}')
    startTime = time.monotonic()
    
    bpy.ops.import_mesh.stl(
        filepath=path)
    if material:
        bpy.context.selected_objects[0].data.materials.append(material)
    
    print(f'Imported in {time.monotonic()-startTime}s')

def import3MF(path: str, useColorGroup: bool, materials:List[bpy.types.Material]):
    print(f'Importing 3MF {path}')
    startTime = time.monotonic()
    
    bpy.ops.import_mesh.threemf(
        filepath=path, use_color_group=useColorGroup)
    mIndex = 0
    if materials:
        for o in bpy.context.selected_objects:
            if len(materials) > 0 and o.data and mIndex < len(o.data.materials):
                print(
                    f'{o.name} has no material assigned so it is assigned material {materials[mIndex]}')
                o.data.materials.append(materials[mIndex])
                mIndex += 1
                
    print(f'Imported in {time.monotonic()-startTime}s')

def importModel(path: str, useColorGroup: bool, materials:List[bpy.types.Material]) -> FileExtensions:
    _, ext = os.path.splitext(path)
    if ext.lower() == FileExtensions.STL.value:
        print(ext.lower())
        importSTL(path=path, material=materials[0] if materials and len(materials) > 0 else None)
        return FileExtensions.STL
    elif ext.lower() == FileExtensions.THREEMF.value:
        import3MF(path=path, useColorGroup=useColorGroup, materials=materials)
        return FileExtensions.THREEMF
    return FileExtensions.UNKNOWN

def exportSTL(path: str):
    print(f'Exporting {len(bpy.data.objects)} objects to STL {path}')
    startTime = time.monotonic()
    
    bpy.ops.export_mesh.stl(
        filepath=path, use_selection=True)
    
    print(f'Exported in {time.monotonic()-startTime}s')

def export3MF(path: str, useColorGroup: bool):
    print(f'Exporting {len(bpy.data.objects)} objects to 3MF {path}')
    startTime = time.monotonic()
    
    bpy.ops.export_mesh.threemf(
        filepath=path, use_selection=True, coordinate_precision=6, use_color_group=True)
    
    print(f'Exported in {time.monotonic()-startTime}s')
    
def exportModel(path: str, useColorGroup: bool):
    _, ext = os.path.splitext(path)
    if ext.lower() == FileExtensions.STL.value:
        print(ext.lower())
        exportSTL(path=path)
    elif ext.lower() == FileExtensions.THREEMF.value:
        export3MF(path=path, useColorGroup=useColorGroup)

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
    import3MF(importPath, addMaterialFromIndex=0,
              use_color_group=use_color_group)


def export3MFTemplate(abbr, scale, printType, style, version, postProcess, partNum):
    bpy.ops.object.select_all(action='DESELECT')

    for o in bpy.data.objects:
        o.select_set(True)

    exportPath = f'{regionsTopDir}{abbr}/{abbr}{"-" if len(scale) > 0 else ""}{scale}-{printType}{"-" if len(style) > 0 else ""}{style}{"-" if len(version) > 0 else ""}{version}{f"-{postProcess}" if postProcess else ""}{f"-p{partNum}" if partNum > 0 else ""}.3mf'
    print(f'Exporting {exportPath}')

    # export objects
    if len(bpy.context.selected_objects) > 0:
        export3MF(exportPath)
