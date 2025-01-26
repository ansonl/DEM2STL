import bpy

from typing import List

def colorTupleFromHexString(s: str) -> tuple[float, ...]:
    return  tuple(float(int(s.lstrip('#')[i:i+2], 16))/255 for i in (0, 2, 4, 6))

# Create hex colors list from the raw color string
def colorTuplesFromHexStrings(colors: List[str]) -> List[tuple]:
    if colors == None:
        return None
    
    colorTuples = []
    for c in colors:
        colorTuples.append(colorTupleFromHexString(c))
    return colorTuples

# Create materials 
def materialsFromColorTuples(colorTuples: List[tuple]) -> List[bpy.types.Material]:
    materials = []
    
    if colorTuples:        
        colorNames = ["Primary", "Secondary"]
        colorIndex = 0
        for t in colorTuples:
            material = bpy.data.materials.new(colorNames[colorIndex] if colorIndex < len(colorNames) else str(colorIndex))
            colorIndex += 1
            materials[0].use_nodes = True
            materials[0].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = t
            materials.append(material)
            print("Created material", colorTuples)
    
    return materials