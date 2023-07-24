import bpy

# Boolean slice

sourceObject, cuttingPath = bpy.data.objects.new( "empty", None )

# Get objections from selection [source, cutting]
if len(bpy.context.selected_objects) == 2:
  sourceObject = bpy.context.selected_objects[0]
  cuttingPath = bpy.context.selected_objects[1]

bpy.ops.object.select_all(action='DESELECT')  

# Manually specify objects by name
"""
cuttingPathName = 'NurbsPath'
sourceObjectName = 'Cube'#'REGION-ABBR-dual-transparent-p1'
bpy.ops.object.select_all(action='DESELECT')

cuttingPath = bpy.data.objects[cuttingPathName]
sourceObject = bpy.data.objects[sourceObjectName]
"""

# convert path to mesh
cuttingPath.select_set(True)
cuttingPath.data.extrude = 50
bpy.ops.object.convert(target='MESH', keep_original=True)
sliceMesh = bpy.data.objects[f'{cuttingPath.name}.001']
sliceMesh.select_set(True)

# duplicate object
sourceObject.select_set(True)
bpy.ops.object.duplicate_move()
dupeObject = bpy.data.objects[f'{sourceObject.name}.001']

# add boolean modifier difference fast
# DIFFERENCE keeps side of object on normal direction of cutting mesh
bool_one = sourceObject.modifiers.new(type="BOOLEAN", name="bool-difference")
bool_one.solver = 'FAST'
bool_one.object = sliceMesh
bool_one.operation = 'DIFFERENCE'

# add boolean modifier intersect fast
bool_one = dupeObject.modifiers.new(type="BOOLEAN", name="bool-intersect")
bool_one.solver = 'FAST'
bool_one.object = sliceMesh
bool_one.operation = 'INTERSECT'

#apply boolean modifier
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = sourceObject
bpy.ops.object.modifier_apply(modifier=sourceObject.modifiers[0].name, report=True)
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = dupeObject
bpy.ops.object.modifier_apply(modifier=dupeObject.modifiers[0].name, report=True)