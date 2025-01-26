import bpy, bmesh, time

print(f'Starting operation')
variantProcessStartTime = time.monotonic()

# Get the active mesh
me = bpy.context.object.data

# Get a BMesh representation
bm = bmesh.new()   # create an empty BMesh
bm.from_mesh(me)   # fill it in from a Mesh

bm.select_flush(True)

for v in bm.verts:
   v.select_set(v.co.z <= 0)

# Finish up, write the bmesh back to the mesh
bm.to_mesh(me)
bm.free()  # free and prevent further access

print(f'operation took {time.monotonic()-variantProcessStartTime}s')