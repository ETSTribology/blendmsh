import bpy
import importlib
from .utils_pip import Pip

class BlendmshPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        Pip._ensure_user_site_package()

        if importlib.util.find_spec('gmsh-api') is not None:
            layout.label(text='gmsh-api loaded.', icon='INFO')
        else:
            layout.label(text='Blendmsh requires gmsh-api!', icon='ERROR')
            layout.operator('blendmsh.installer', text="Install gmsh-api")


class BlendmshInstaller(bpy.types.Operator):
    bl_idname = "blendmsh.installer"
    bl_label = "Install gmsh-api"
    bl_description = "Install gmsh-api via pip"

    def execute(self, context):
        try:
            Pip.install('gmsh-api')
            import gmsh_api
            self.report({'INFO'}, f'Successfully installed gmsh-api {gmsh_api.__version__}.')
        except ModuleNotFoundError:
            self.report({'ERROR'}, 'Could not install gmsh-api, please install manually.')
        return {'FINISHED'}
