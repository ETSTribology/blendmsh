import bpy
import importlib

class BlendmshPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout

        try:
            import pygmsh
            self.report({'INFO'}, f'Vendorized pygmsh loaded successfully.')
            return {'FINISHED'}
        except ImportError as e:
            self.report({'ERROR'}, 'Failed to load pygmsh from _vendor. Ensure the vendorized library is installed correctly.')
            return {'CANCELLED'}
