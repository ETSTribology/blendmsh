import bpy
import importlib

class BlendmshPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout

        # Check if the vendorized 'gmsh-api' exists within the add-on
        if importlib.util.find_spec('.gmsh_api', package=__package__) is not None:
            layout.label(text='gmsh-api (vendorized) loaded.', icon='INFO')
        else:
            layout.label(text='gmsh-api not found in _vendor!', icon='ERROR')


class BlendmshInstaller(bpy.types.Operator):
    bl_idname = "blendmsh.installer"
    bl_label = "Install gmsh-api"
    bl_description = "Install gmsh-api via pip"

    def execute(self, context):
        try:
            # Use the vendorized version of gmsh-api
            from ._vendor.gmsh_api import gmsh
            self.report({'INFO'}, f'Vendorized gmsh-api {gmsh.__version__} loaded.')
            return {'FINISHED'}
        except ImportError as e:
            self.report({'ERROR'}, 'Failed to load gmsh-api from _vendor.')
            return {'CANCELLED'}
