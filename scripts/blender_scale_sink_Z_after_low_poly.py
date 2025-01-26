# scale up all vertices Z by 300% and correct base level back to original base level
for v in bpy.context.active_object.data.vertices:
    if v.co.z > 0:
        v.co.z *= 3
        v.co.z -= 1.8