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
from .preferences import BlendmshPreferences, BlendmshInstaller

def register():
    bpy.utils.register_class(BlendmshPreferences)
    bpy.utils.register_class(BlendmshInstaller)
    bpy.utils.register_class(BlendmshProperties)
    bpy.utils.register_class(BLENDMSH_PT_Panel)
    
    bpy.types.Scene.blendmsh = bpy.props.PointerProperty(type=BlendmshProperties)
    
    bpy.utils.register_class(BLENDMSH_OT_Meshinit)
    bpy.utils.register_class(BLENDMSH_OT_Meshproc)
    bpy.utils.register_class(BLENDMSH_OT_Physicalgroups)

def unregister():
    bpy.utils.unregister_class(BlendmshPreferences)
    bpy.utils.unregister_class(BlendmshInstaller)
    bpy.utils.unregister_class(BlendmshProperties)
    bpy.utils.unregister_class(BLENDMSH_PT_Panel)
    bpy.utils.unregister_class(BLENDMSH_OT_Meshinit)
    bpy.utils.unregister_class(BLENDMSH_OT_Meshproc)
    bpy.utils.unregister_class(BLENDMSH_OT_Physicalgroups)

if __name__ == "__main__":
    register()
