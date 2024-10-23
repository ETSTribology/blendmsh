bl_info = {
    "name": "Blendmsh",
    "author": "Senthur Raj",
    "description": "Blendmsh is a bridge between Blender and Gmsh, a 3D finite element mesh generator.",
    "blender": (4, 2, 0),
    "version": (1, 1, 0),
    "location": "View3D > Sidebar > Blendmsh",
    "category": "Mesh",
}

import bpy

from .properties import BlendmshProperties
from .panel import BLENDMSH_PT_Panel
from .processor import BLENDMSH_OT_Meshinit, BLENDMSH_OT_Meshproc, BLENDMSH_OT_Physicalgroups
from .preferences import BlendmshPreferences

classes = (
    BlendmshPreferences,
    BlendmshProperties,
    BLENDMSH_PT_Panel,
    BLENDMSH_OT_Meshinit,
    BLENDMSH_OT_Meshproc,
    BLENDMSH_OT_Physicalgroups,
)

def register():
    try:
        for cls in classes:
            bpy.utils.register_class(cls)

        # Register custom property to Scene
        bpy.types.Scene.blendmsh = bpy.props.PointerProperty(type=BlendmshProperties)

    except Exception as e:
        print(f"Error during registration: {e}")
        unregister()  # Clean up if registration fails

def unregister():
    try:
        # Unregister in reverse order to avoid dependency issues
        del bpy.types.Scene.blendmsh
        for cls in reversed(classes):
            bpy.utils.unregister_class(cls)
    except Exception as e:
        print(f"Error during unregistration: {e}")

if __name__ == "__main__":
    register()
