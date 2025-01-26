import bpy

# Setup scene for 3d print export
def setupScene():
    # Delete any existing objects
    for o in bpy.data.objects:
        o.select_set(True)
    bpy.ops.object.delete()

    # set scene from m to mm
    bpy.data.scenes["Scene"].unit_settings.scale_length = 0.001

# Clean up scene after deleting objects
def cleanUpScene():
    bpy.ops.outliner.orphans_purge() # purge remaining mesh left behind by object, this also deletes materials
        
# Try to make object manifold
def checkAndRepairNonSolid(targetObject):
    if targetObject.data is None:
        print(f'{targetObject.name} data is none. Skipping repair the object.')
        return
  
    bpy.context.view_layer.objects.active = targetObject
    
    print(f'Making object manifold')
    
    bpy.ops.mesh.print3d_clean_non_manifold()
    
    print(f'Finished object manifold')