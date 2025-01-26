# decimate bottom inner vertices to 1%
import bpy, time

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
