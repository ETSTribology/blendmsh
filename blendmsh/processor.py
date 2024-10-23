import bpy
import os
from collections import OrderedDict
import pygmsh

class BLENDMSH_OT_Physicalgroups(bpy.types.Operator):
    bl_idname = "blendmsh.physicalgroups"
    bl_label = "Create Physical Groups"

    diffuse_library = [
        (1.0, 0.0, 0.78, 1),  # Magenta
        (1.0, 0.97, 0.0, 1),  # Yellow
        (0.32, 1.0, 0.0, 1),  # Green
        (0.05, 0.85, 0.52, 1),  # Aqua
        (0.45, 1.0, 0.0, 1),  # Lime
        (0.0, 0.85, 1.0, 1),  # Cyan
        (0.92, 1.0, 0.0, 1),  # Light Yellow
        (1.0, 0.7, 0.32, 1),  # Orange
        (0.58, 0.05, 0.34, 1),  # Red
        (1.0, 0.0, 0.55, 1),  # Hot Pink
        (1.0, 0.54, 0.0, 1)   # Dark Orange
    ]

    def execute(self, context):
        scene = context.scene
        active_object = context.active_object

        if not scene.blendmsh.initialized:
            self.report({'ERROR'}, 'Initialize the mesh before defining physical groups.')
            return {'CANCELLED'}

        if active_object is None or active_object.type != 'MESH':
            self.report({'ERROR'}, 'No active mesh object found.')
            return {'CANCELLED'}

        # Ensure 'NATIVE' material exists
        if 'NATIVE' not in bpy.data.materials:
            native_mat = bpy.data.materials.new(name='NATIVE')
            active_object.data.materials.append(native_mat)

        # Create materials for physical groups
        for i in range(scene.blendmsh.n_physicalgroups):
            group_name = f'GROUP_{i+1}'
            if group_name not in bpy.data.materials:
                temp_mat = bpy.data.materials.new(name=group_name)
                temp_mat.diffuse_color = self.diffuse_library[i % len(self.diffuse_library)]
                active_object.data.materials.append(temp_mat)

        self.report({'INFO'}, f'{scene.blendmsh.n_physicalgroups} physical groups created.')
        return {'FINISHED'}


class BLENDMSH_OT_Meshinit(bpy.types.Operator):
    bl_idname = 'blendmsh.meshinit'
    bl_label = 'Initialize Mesh'
    bl_description = 'Triangulates the active object and prepares it for meshing.'

    def execute(self, context):
        scene = context.scene
        active_object = context.active_object

        if active_object is None or active_object.type != 'MESH':
            self.report({'ERROR'}, 'No valid mesh object to initialize.')
            return {'CANCELLED'}

        try:
            if active_object.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')

            # Set shading to MATERIAL for better visualization
            if context.space_data.type == 'VIEW_3D':
                context.space_data.shading.type = 'MATERIAL'

            filename = active_object.name + '.stl'
            filepath = os.path.join(scene.blendmsh.workspace_path, filename)

            bpy.ops.wm.stl_export(filepath=filepath, ascii_format=True)

            if not os.path.exists(filepath):
                self.report({'ERROR'}, f"Failed to export '{filename}' to '{scene.blendmsh.workspace_path}'.")
                return {'CANCELLED'}

            bpy.ops.object.select_all(action='DESELECT')
            active_object.select_set(True)
            bpy.ops.object.delete()

            bpy.ops.wm.stl_import(filepath=filepath)
            new_object = context.active_object

            if new_object is None or new_object.type != 'MESH':
                self.report({'ERROR'}, 'Failed to re-import the STL file.')
                return {'CANCELLED'}

            native_mat = bpy.data.materials.get('NATIVE')
            if native_mat is None:
                native_mat = bpy.data.materials.new(name='NATIVE')
            new_object.data.materials.append(native_mat)

            scene.blendmsh.initialized = True
            self.report({'INFO'}, f'Mesh initialized for {new_object.name}.')
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f'Failed to initialize mesh: {str(e)}.')
            return {'CANCELLED'}


class BLENDMSH_OT_Meshproc(bpy.types.Operator):
    bl_idname = 'blendmsh.meshproc'
    bl_label = 'Process Mesh'
    bl_description = 'Processes the mesh and generates the finite element mesh using pygmsh.'

    def execute(self, context):
        scene = context.scene
        active_object = context.active_object

        if not scene.blendmsh.initialized:
            self.report({'ERROR'}, 'Mesh has not been initialized.')
            return {'CANCELLED'}

        try:
            from .. import pygmsh

            filename = active_object.name + '.stl'
            filepath = os.path.join(scene.blendmsh.workspace_path, filename)

            if not os.path.exists(filepath):
                self.report({'ERROR'}, f'STL file "{filepath}" not found.')
                return {'CANCELLED'}

            geom = pygmsh.geo.Geometry()
            with open(filepath, 'r') as f:
                stl_content = f.read()

            # Process the STL mesh and generate the Gmsh mesh
            geom.add_stl(stl_content, lcar=scene.blendmsh.cl_max)

            mesh = pygmsh.generate_mesh(geom, verbose=True, geo_filename=filepath)
            output_file = os.path.join(scene.blendmsh.workspace_path, filename + scene.blendmsh.output_file_format)

            mesh.write(output_file)

            self.report({'INFO'}, f'Mesh written to {output_file}.')
            return {'FINISHED'}

        except ImportError:
            self.report({'ERROR'}, 'Could not import pygmsh. Please ensure it is installed.')
            return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f'Error processing mesh: {str(e)}.')
            return {'CANCELLED'}

    @staticmethod
    def get_raw_data(path):
        """Extracts raw vertex data from an STL file."""
        data = []
        try:
            with open(path, 'r') as file:
                current_tri = []
                for line in file:
                    if 'vertex' in line:
                        vertex = tuple(map(float, line.strip().split()[1:]))
                        current_tri.append(vertex)
                    if 'endfacet' in line:
                        data.append(tuple(current_tri))
                        current_tri = []
            return data
        except Exception as e:
            raise IOError(f"Error reading STL file: {e}")
