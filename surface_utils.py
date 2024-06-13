# surface_utils.py
import bpy                                                                       # type: ignore
import math
from mathutils import Vector                                    # type: ignore
from math import sin, cos

def evaluate_formula(u, v, formula_x, formula_y, formula_z):
    try:
        x = eval(formula_x, {'u': u, 'v': v, 'math': math, 'sin': sin, 'cos': cos})
        y = eval(formula_y, {'u': u, 'v': v, 'math': math, 'sin': sin, 'cos': cos})
        z = eval(formula_z, {'u': u, 'v': v, 'math': math, 'sin': sin, 'cos': cos})
        return x, y, z
    except Exception as e:
        print("Ошибка в формулах:", e)
        return None

def generate_surface(scale, subdivisions, formula_x, formula_y, formula_z):
    verts = []
    for i in range(subdivisions + 1):
        for j in range(subdivisions + 1):
            u = scale * (i / subdivisions)
            v = scale * (j / subdivisions)
            result = evaluate_formula(u, v, formula_x, formula_y, formula_z)
            if result is not None:
                verts.append(Vector(result))
            else:
                print(f"Ошибка в вычислении для u={u}, v={v}")

    if len(verts) == 1:
        print(" Нвфе удалось создать вершины. Проверьте уравнения и параметры.")
        return

    faces = []
    for i in range(subdivisions):
        for j in range(subdivisions):
            v1 = i * (subdivisions + 1) + j
            v2 = v1 + 1
            v3 = (i + 1) * (subdivisions + 1) + j
            v4 = v3 + 1
            faces.append((v1, v2, v4, v3))

    mesh = bpy.data.meshes.new(name="Поверхность по уравнению")
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    obj = bpy.data.objects.new("Поверхность по уравнению", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
