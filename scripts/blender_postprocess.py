# duplicate object

# add boolean modifier difference fast

# add boolean modifier intersect fast

# for each add'l curve mesh

# duplicate object that had intersect modifier

# add boolean modifier difference fast

# add boolean modifier intersect fast

# select objects
objectsToExport = ["REGION-ABBR-dual-transparent-p1"]

bpy.ops.object.select_all(action='DESELECT')

for o in bpy.data.objects:
    # Check for given object names
    if o.name in objectsToExport:
        o.select_set(True)

# export objects
bpy.ops.export_mesh.threemf(filepath="K:\USAofPlasticv1\release_250m_v1\CA\CA-dual-transparent-p2.3mf", use_selection=True)