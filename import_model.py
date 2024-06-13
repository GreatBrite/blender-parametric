# import_model.py
import bpy                                                                                                                      # type: ignore

def import_model(filepath):
    verts = []
    faces = []
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('v '):
                _, x, y, z = line.strip().split()
                verts.append((float(x), float(y), float(z)))
            elif line.startswith('f '):
                face_indices = line.strip().split()[1:]
                if len(face_indices) == 3:
                    faces.append(tuple(int(vi) - 1 for vi in face_indices))
                elif len(face_indices) == 4:
                    v1, v2, v3, v4 = (int(vi) - 1 for vi in face_indices)
                    faces.append((v1, v2, v3))
                    faces.append((v1, v3, v4))
                else:
                    print("Обнаружен полигон с более чем 4 вершинами.")

    mesh = bpy.data.meshes.new(name="Импортированная модель")
    mesh.from_pydata(verts, [], faces)
    obj = bpy.data.objects.new("Импортированная модель", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


