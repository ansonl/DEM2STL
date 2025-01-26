import bpy, time

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