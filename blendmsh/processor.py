import bpy
import os
from collections import OrderedDict

class BLENDMSH_OT_Physicalgroups(bpy.types.Operator):
    bl_idname = "blendmsh.physicalgroups"
    bl_label = "Create Physical Groups"

    # Improved color library for physical groups
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
        active_object = bpy.context.active_object

        if scene.blendmsh.initialized:
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
                    temp_mat.diffuse_color = self.diffuse_library[i % len(self.diffuse_library)]  # Avoid index overflow
                    active_object.data.materials.append(temp_mat)

            self.report({'INFO'}, f'{scene.blendmsh.n_physicalgroups} physical groups created.')
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, 'Initialize the mesh before defining physical groups.')
            return {'CANCELLED'}


class BLENDMSH_OT_Meshinit(bpy.types.Operator):
    bl_idname = 'blendmsh.meshinit'
    bl_label = 'Initialize Mesh'
    bl_description = 'Triangulates the active object and prepares it for meshing.'

    def execute(self, context):
        scene = context.scene
        active_object = bpy.context.active_object

        if active_object is None or active_object.type != 'MESH':
            self.report({'ERROR'}, 'No valid mesh object to initialize.')
            return {'CANCELLED'}

        try:
            # Ensure the object is in Object Mode for operations
            if active_object.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')

            # Set shading to MATERIAL for better visualization
            bpy.context.space_data.shading.type = 'MATERIAL'

            filename = active_object.name + '.stl'
            filepath = os.path.join(scene.blendmsh.workspace_path, filename)

            # Export the object as STL
            bpy.ops.wm.stl_export(filepath=filepath, ascii=True)

            # Check if the file was exported successfully
            if not os.path.exists(filepath):
                self.report({'ERROR'}, f"Failed to export '{filename}' to '{scene.blendmsh.workspace_path}'.")
                return {'CANCELLED'}

            # Delete original object
            bpy.ops.object.select_all(action='DESELECT')
            active_object.select_set(True)
            bpy.ops.object.delete()

            # Re-import the STL
            bpy.ops.import_mesh.stl(filepath=filepath)
            new_object = bpy.context.active_object

            if new_object is None or new_object.type != 'MESH':
                self.report({'ERROR'}, 'Failed to re-import the STL file.')
                return {'CANCELLED'}

            # Apply 'NATIVE' material
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
    bl_description = 'Processes the mesh and generates the finite element mesh using Gmsh.'

    def execute(self, context):
        scene = context.scene
        active_object = bpy.context.active_object

        if not scene.blendmsh.initialized:
            self.report({'ERROR'}, 'Mesh has not been initialized.')
            return {'CANCELLED'}

        try:
            from ._vendor.gmsh_api import gmsh

            filename = active_object.name + '.stl'
            filepath = os.path.join(scene.blendmsh.workspace_path, filename)

            # Check if the STL file exists
            if not os.path.exists(filepath):
                self.report({'ERROR'}, f'STL file "{filepath}" not found.')
                return {'CANCELLED'}

            # Read mesh data
            data = self.get_raw_data(filepath)

            # Initialize gmsh and create geometry
            gmsh.initialize()
            gmsh.option.setNumber('General.Terminal', 1)
            geo = gmsh.model.geo
            points = OrderedDict()
            triangles = OrderedDict()
            edges = OrderedDict()

            # Process vertices and create points
            i = 1
            for surface in data:
                for vertex in surface:
                    if vertex not in points:
                        points[vertex] = i
                        geo.addPoint(vertex[0], vertex[1], vertex[2], scene.blendmsh.cl_max, i)
                        i += 1

            # Generate triangles and edges
            i = 1
            for triangle in data:
                point_ids = [points[vertex] for vertex in triangle]
                triangles[i] = point_ids
                i += 1

            # Define curves and surfaces
            for tri_id, tri in triangles.items():
                curve_loop = []
                for j in range(3):
                    v1, v2 = tri[j], tri[(j + 1) % 3]
                    if (v1, v2) not in edges and (v2, v1) not in edges:
                        edge_id = len(edges) + 1
                        geo.addLine(v1, v2, edge_id)
                        edges[(v1, v2)] = edge_id
                    edge_id = edges.get((v1, v2), edges.get((v2, v1)))
                    curve_loop.append(edge_id)
                geo.addCurveLoop(curve_loop, tri_id)
                geo.addPlaneSurface([tri_id], tri_id)

            # Synchronize and generate mesh
            gmsh.model.geo.synchronize()
            gmsh.model.mesh.generate(int(scene.blendmsh.mesh_dimension))

            # Write the mesh to the specified format
            output_file = os.path.join(scene.blendmsh.workspace_path, filename + scene.blendmsh.output_file_format)
            gmsh.write(output_file)
            gmsh.finalize()

            self.report({'INFO'}, f'Mesh written to {output_file}.')
            return {'FINISHED'}

        except ImportError:
            self.report({'ERROR'}, 'Could not import Gmsh module. Please ensure it is installed.')
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
