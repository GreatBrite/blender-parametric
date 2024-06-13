# mesh_operations.py
import bpy

def triangulate_mesh(obj):
    if obj.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT')

def save_triangulated_mesh(filepath, obj):
    with open(filepath, 'w') as file:
        file.write("# OBJ файл\n")
        for v in obj.data.vertices:
            file.write(f"v {v.co.x} {v.co.y} {v.co.z}\n")
        for poly in obj.data.polygons:
            if len(poly.vertices) == 3:
                verts = [str(vi + 1) for vi in poly.vertices]
                file.write(f"f {' '.join(verts)}\n")
            elif len(poly.vertices) == 4:
                v1, v2, v3, v4 = [str(vi + 1) for vi in poly.vertices]
                file.write(f"f {v1} {v2} {v3}\n")
                file.write(f"f {v1} {v3} {v4}\n")
            else:
                print("Обнаружен полигон с более чем 4 вершинами.")
                