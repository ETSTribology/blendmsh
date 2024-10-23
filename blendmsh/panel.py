# panel.py
import bpy

class BLENDMSH_PT_Panel(bpy.types.Panel):
    bl_idname = 'BLENDMSH_PT_panel'
    bl_label = 'Blendmsh'
    bl_category = 'Blendmsh'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene.blendmsh, 'workspace_path', text="Workspace Path")

        layout.operator('blendmsh.meshinit', text='Initialize Mesh')

        layout.prop(scene.blendmsh, "n_physicalgroups", text="Physical Groups")
        layout.operator('blendmsh.physicalgroups', icon='ADD', text="Add Groups")

        layout.prop(scene.blendmsh, "element_order", text="Element Order")
        layout.prop(scene.blendmsh, 'algorithm', text="Meshing Algorithm")
        layout.prop(scene.blendmsh, "cl_max", text="Element Size")
        layout.prop(scene.blendmsh, "mesh_dimension", text="Mesh Dimension")
        layout.prop(scene.blendmsh, 'output_file_format', text="Output Format")

        layout.operator('blendmsh.meshproc', text='Generate Mesh')
