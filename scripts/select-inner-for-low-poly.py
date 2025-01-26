import bpy, time

#desired_threshold_border = 0.001
desired_threshold = 0.002

scaleZ = 3

modelBaseThicknessAtSeaLevel = 0.9
sinkDownZ = 0.9*(scaleZ-1)

# print Status

print(f'Starting low polyization')
variantProcessStartTime = time.monotonic()

originalVertexCount = 0
for obj in bpy.context.scene.objects:
    originalVertexCount += len(obj.data.vertices)
    
print(f'Original vertex count {originalVertexCount}')

# decimate bottom

for e in [bpy.context.active_object.data.vertices, bpy.context.active_object.data.polygons, bpy.context.active_object.data.edges]:
    e.foreach_set("select", (False,)*len(e))

for v in bpy.context.active_object.data.vertices:
   v.select = v.co.z <= 0
   
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_less()
   
bpy.ops.object.vertex_group_assign_new()
bpy.context.active_object.vertex_groups[0].name = 'bottom-inner'   

bpy.ops.object.modifier_add(type='DECIMATE')
bpy.context.object.modifiers["Decimate"].vertex_group='bottom-inner'
bpy.context.object.modifiers["Decimate"].ratio=0.01
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.modifier_apply(modifier='Decimate')

#bpy.ops.object.mode_set(mode='OBJECT')
#print(f'select inner bottom and decimate took {time.monotonic()-variantProcessStartTime}s')

# select inner land without outer border to merge

for v in bpy.context.active_object.data.vertices:
   v.select = v.co.z <= 0

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_more()

inset_steps = 20

for _ in range(inset_steps):
    bpy.ops.mesh.select_more()


bpy.ops.mesh.select_all(action='INVERT')

recalculated_threshold = desired_threshold / bpy.context.scene.unit_settings.scale_length

bpy.ops.mesh.remove_doubles(threshold=recalculated_threshold, use_unselected=False)

bpy.ops.object.mode_set(mode='OBJECT')


# scale up all vertices Z by 300% and correct base level back to original base level

for obj in bpy.context.scene.objects:
    for v in obj.data.vertices:
        if v.co.z > 0:
            v.co.z *= scaleZ
            v.co.z -= sinkDownZ
        
# print Status

endVertexCount = 0
for obj in bpy.context.scene.objects:
    endVertexCount += len(obj.data.vertices)

print(f'End vertex count {endVertexCount} - {endVertexCount/originalVertexCount*100}% of original vertex count')        

print(f'low poly took {time.monotonic()-variantProcessStartTime}s')

'''
# select inner land with outer border to merge

for v in bpy.context.active_object.data.vertices:
   v.select = v.co.z <= 0

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_more()

inset_steps_border = 10

for _ in range(inset_steps_border):
    bpy.ops.mesh.select_more()

bpy.ops.mesh.select_all(action='INVERT')

recalculated_threshold = desired_threshold_border / bpy.context.scene.unit_settings.scale_length

bpy.ops.mesh.remove_doubles(threshold=recalculated_threshold, use_unselected=False)

bpy.ops.object.mode_set(mode='OBJECT')
'''

'''
# select inner land without outer border to merge

for v in bpy.context.active_object.data.vertices:
   v.select = v.co.z <= 0

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_more()

inset_steps = round(desired_threshold/desired_threshold_border)

for _ in range(inset_steps):
    bpy.ops.mesh.select_more()


bpy.ops.mesh.select_all(action='INVERT')

recalculated_threshold = desired_threshold / bpy.context.scene.unit_settings.scale_length

bpy.ops.mesh.remove_doubles(threshold=recalculated_threshold, use_unselected=False)

bpy.ops.object.mode_set(mode='OBJECT')
'''

#bpy.ops.object.modifier_add(type='DECIMATE')

#bpy.ops.object.vertex_group_assign_new()
#bpy.context.active_object.vertex_groups[0].name = 'inner-land'

