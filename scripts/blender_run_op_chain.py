import re

from map_utils.argument import *
from map_utils.materials import *
from map_utils.import_export import *
from map_utils.scene import *
from map_utils.decimate_bottom_inner_vertices import *
from map_utils.merge_top_inner_vertices import *

# & 'C:\Program Files\Blender Foundation\Blender 3.5\blender.exe' -b --python .\blender_run_op_chain.py -- -mode manual -inputFiles C:\Users\ansonl\development\dem-to-stl-workflow\state_stls\usa-individual-states-sqrt\250\DC\DC_tile_1_1.STL -outputFile C:\Users\ansonl\development\dem-to-stl-workflow\state_stls\usa-individual-states-sqrt\250\DC\DC_tile_1_1_decim_bot.STL -ops checkAndRepairNonSolid decimateBottomInnerVertices

# & 'C:\Program Files\Blender Foundation\Blender 3.5\blender.exe' --python .\blender_run_op_chain.py -- -mode manual -inputFiles C:\Users\ansonl\development\dem-to-stl-workflow\state_stls\usa-individual-states-sqrt\250\DC\DC_tile_1_1.STL -outputFile C:\Users\ansonl\development\dem-to-stl-workflow\state_stls\usa-individual-states-sqrt\250\DC\DC_tile_1_1_decim_bot.STL -ops checkAndRepairNonSolid decimateBottomInnerVertices

# & 'C:\Program Files\Blender Foundation\Blender 3.5\blender.exe' --python .\blender_run_op_chain.py -- -mode manual -inputFiles C:\Users\ansonl\development\dem-to-stl-workflow\state_stls\usa-individual-states-sqrt\250\MD\MD_tile_1_1.STL -outputFile C:\Users\ansonl\development\dem-to-stl-workflow\state_stls\usa-individual-states-sqrt\250\MD\MD_tile_1_1_output.STL -ops checkAndRepairNonSolid decimateBottomInnerVertices mergeTopInnerVertices

# & 'C:\Program Files\Blender Foundation\Blender 3.5\blender.exe' -b --python .\blender_run_op_chain.py -- -mode autoTemplateDir -inputDirectory C:\Users\ansonl\development\dem-to-stl-workflow\state_stls\usa-individual-states-sqrt\250\

# Whitelisted operations we can call directly
operationWhiteList = [checkAndRepairNonSolid, decimateBottomInnerVertices, mergeTopInnerVertices]

# Read Arguments
args = readArguments()

mode = ProcessingMode.mode(input=args.mode)

# Manual mode
manualImportFilePaths: List[str] = args.inputFiles
manualExportFilePath: str = args.outputFile
print(manualImportFilePaths)

# Auto mode
inputTopDir: str = args.inputDirectory
eScaleTitle: str = args.eScaleLabel
versions: List[str] = []
versions.append(args.version)
versions.append(args.newVersion)

# Shared
materials: List[bpy.types.Material] = materialsFromColorTuples(colorTuples=colorTuplesFromHexStrings(colors=args.colors))
userOperations: List[str] = args.ops

# Setup the scene
setupScene()

def runOperationsOnObject(operations: List[str], object: bpy.types.Object):  
    for op in operations:
        print(f'Running {op} on {object.name}')
        opFunction = globals()[op]
        if opFunction in operationWhiteList:
            opFunction(object)
        else:
            raise Exception(f'Operation {op} is not whitelisted')
        #object.select_set(False)
    
def exportAllFiles(path: str):
    for o in bpy.data.objects:
        o.select_set(True)
    
    if len(bpy.context.selected_objects) > 0:
        exportModel(path=path, useColorGroup=True)
    print(f'Finished with manual mode 3MF export')
    
def execute(mode: ProcessingMode):
    if mode == ProcessingMode.MANUAL:
        for path in manualImportFilePaths:
            importModel(path, useColorGroup=True, materials=materials)
    
        for obj in bpy.data.objects:
            runOperationsOnObject(operations=userOperations, object=obj)
            
        exportAllFiles(path=manualExportFilePath)
        
        bpy.ops.object.delete()  # delete the object afterwards to reduce unused memory usage
        cleanUpScene()
        
    elif mode == ProcessingMode.AUTO_TEMPLATE_DIR:
        inputFileExtension = FileExtensions.STL
        outputFileExtension = FileExtensions.THREEMF
        
        os.chdir(inputTopDir)
        subDirs = os.listdir(inputTopDir)
        excludeList = []

        def get_dir_size(path='.', modelFileType: FileExtensions=FileExtensions.UNKNOWN, excludeRegex: str = ''):
            total = 0
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        # Count only matching file extension
                        if modelFileType == FileExtensions.UNKNOWN or entry.name.lower().endswith(modelFileType.value):
                            total += entry.stat().st_size
                        
                        # Exclude directories that have files that match the regex
                        if len(excludeRegex) > 0 and re.search(pattern=excludeRegex, string=entry.name):
                            excludeDir = path[path.rfind('/')+1:]
                            excludeList.append(excludeDir)
                            print(f'Excluding {excludeDir} after finding {entry.name}')
                    elif entry.is_dir():
                        total += get_dir_size(entry.path)
                        print(f'Added sub dir {entry.path} size to {path} size')
            return total


        subDirs.sort(key=lambda f: get_dir_size(path=inputTopDir+f, modelFileType=inputFileExtension, excludeRegex=''), reverse=False)

        print(subDirs)

        for subDir in subDirs:
            
            if subDir in excludeList:
                print(f'Skipping {subDir} from the exclude list.')
                continue
            
            with os.scandir(subDir) as it:
                for entry in it:
                    print(entry)
                    pass
                    
                    if entry.is_file() and entry.name.endswith(inputFileExtension.value):
                        importModel(path=inputTopDir+subDir, useColorGroup=True, materials=materials)
            
            #processEntry(rAbbr, scaleTitle, versionTitle, newVersionTitle)

execute(mode=mode)