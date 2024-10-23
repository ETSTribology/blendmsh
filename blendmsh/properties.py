import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, EnumProperty, BoolProperty

class BlendmshProperties(bpy.types.PropertyGroup):
    initialized: BoolProperty(default=False)

    workspace_path: StringProperty(
        name="Workspace Path",
        description="Path where mesh results are stored",
        default='/tmp/',
        subtype='DIR_PATH'
    )

    cl_max: FloatProperty(
        name="Element Size",
        default=0.1,
        min=0.1,
        max=5.0,
        precision=3,
        description="Maximum size of the mesh element."
    )

    n_physicalgroups: IntProperty(
        name="Physical Groups",
        default=0,
        min=0,
        description="Number of physical groups."
    )

    element_order: EnumProperty(
        name='Element Order',
        items=[('1', '1', 'First Order'), ('2', '2', 'Second Order')],
        default='1'
    )

    mesh_dimension: EnumProperty(
        name='Mesh Dimension',
        items=[('2', '2D', '2D Mesh'), ('3', '3D', '3D Mesh')],
        default='3'
    )

    algorithm: EnumProperty(
        name='Meshing Algorithm',
        items=[('0', 'Auto', 'Automatic Meshing')],
        default='0'
    )

    output_file_format : EnumProperty(
                name='Output',
                items=[
                        ('.msh', '.msh', 'Gmsh (.msh)'),
                        ('.inp', '.inp', 'Abaqus (.inp)'),
                        ('.vtk', '.vtk', 'The Visualization Toolkit (.vtk)')],
                default='.msh',
                description='Output file format')
