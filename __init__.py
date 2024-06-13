# __init__.py
import bpy                                                                          
from bpy.types import Operator, Panel                                                                           
from bpy.props import StringProperty, FloatProperty, IntProperty                                                                          
from bpy_extras.io_utils import ImportHelper                                                                                                
from bpy_extras.object_utils import AddObjectHelper                                                                          
from .surface_utils import evaluate_formula, generate_surface
from .mesh_operations import triangulate_mesh, save_triangulated_mesh
from .import_model import import_model

bl_info = {
    "name": "Инструменты поверхности и модели",
    "author": "BritkovVV",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "3D View > Панель > Инструменты поверхности и модели",
    "description": "Создание поверхности из уравнений и импорт моделей",
    "category": "Add Mesh",
}

def add_surface_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_surface.bl_idname,
        text="Добавить поверхность по уравнениям",
        icon='MESH_PLANE'
    )

def add_surface_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/ru/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_surface", "modeling/meshes/primitives/surface.html"),
    )
    return url_manual_prefix, url_manual_mapping

def register():
    bpy.utils.register_class(OBJECT_OT_add_surface)
    bpy.utils.register_class(OBJECT_OT_triangulate_surface)
    bpy.utils.register_class(OBJECT_OT_import_model)
    bpy.utils.register_class(OBJECT_OT_save_triangulated)
    bpy.utils.register_class(PANEL_PT_add_surface)
    bpy.utils.register_manual_map(add_surface_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_surface_button)
    bpy.types.Scene.surface_equation_scale = bpy.props.FloatProperty(name="Масштаб", default=10.0, min=0.01)
    bpy.types.Scene.surface_equation_subdivisions = bpy.props.IntProperty(name="Подразделения", default=100, min=1)
    bpy.types.Scene.surface_equation_formula_x = bpy.props.StringProperty(name="X(u,v)", default="u")
    bpy.types.Scene.surface_equation_formula_y = bpy.props.StringProperty(name="Y(u,v)", default="v")
    bpy.types.Scene.surface_equation_formula_z = bpy.props.StringProperty(name="Z(u,v)", default="0")

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_surface)
    bpy.utils.unregister_class(OBJECT_OT_triangulate_surface)
    bpy.utils.unregister_class(OBJECT_OT_import_model)
    bpy.utils.unregister_class(OBJECT_OT_save_triangulated)
    bpy.utils.unregister_class(PANEL_PT_add_surface)
    bpy.utils.unregister_manual_map(add_surface_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_surface_button)
    del bpy.types.Scene.surface_equation_scale
    del bpy.types.Scene.surface_equation_subdivisions
    del bpy.types.Scene.surface_equation_formula_x
    del bpy.types.Scene.surface_equation_formula_y
    del bpy.types.Scene.surface_equation_formula_z

class OBJECT_OT_add_surface(Operator, AddObjectHelper):
    """Создать новую поверхность из уравнений"""
    bl_idname = "mesh.add_surface"
    bl_label = "Добавить поверхность по уравнениям"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scale = context.scene.surface_equation_scale
        subdivisions = context.scene.surface_equation_subdivisions
        formula_x = context.scene.surface_equation_formula_x
        formula_y = context.scene.surface_equation_formula_y
        formula_z = context.scene.surface_equation_formula_z
        generate_surface(scale, subdivisions, formula_x, formula_y, formula_z)
        return {'FINISHED'}

class OBJECT_OT_triangulate_surface(Operator):
    """Триангулировать поверхность"""
    bl_idname = "mesh.triangulate_surface"
    bl_label = "Триангулировать поверхность"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        triangulate_mesh(context.active_object)
        return {'FINISHED'}

class OBJECT_OT_import_model(Operator, ImportHelper):
    """Импортировать модель"""
    bl_idname = "import_scene.import_model"
    bl_label = "Импорт модели"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".obj"

    filter_glob: StringProperty(
        default="*.obj;*.txt",  
        options={'HIDDEN'},
        maxlen=255, 
    )                                                                                                      

    def execute(self, context):
        import_model(self.filepath)
        return {'FINISHED'}

    def execute(self, context):
        import_model(self.filepath)
        return {'FINISHED'}

class OBJECT_OT_save_triangulated(Operator, ImportHelper):
    """Сохранить поверхность"""
    bl_idname = "export_scene.save_triangulated"
    bl_label = "Сохранить поверхность"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".obj"

    filter_glob: StringProperty(
        default="*.obj",
        options={'HIDDEN'},
        maxlen=255,  
    )                                                                          

    def execute(self, context):
        save_triangulated_mesh(self.filepath, context.active_object)
        return {'FINISHED'}

class PANEL_PT_add_surface(Panel):
    """Панель добавления поверхности"""
    bl_label = "Поверхность"
    bl_idname = "PANEL_PT_add_surface"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Инструменты поверхности и модели'

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.prop(scene, "surface_equation_scale")
        layout.prop(scene, "surface_equation_subdivisions")
        layout.prop(scene, "surface_equation_formula_x")
        layout.prop(scene, "surface_equation_formula_y")
        layout.prop(scene, "surface_equation_formula_z")

        layout.operator("mesh.add_surface")
        layout.operator("mesh.triangulate_surface")
        layout.operator("import_scene.import_model")
        layout.operator("export_scene.save_triangulated")

if __name__ == "__main__":
    register()
