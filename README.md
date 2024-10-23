# Blendmsh
[![Blender](https://img.shields.io/badge/Blender-4.20%2B-orange)](https://www.blender.org/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6ffbb6b533d044d590498fb4d730999b)](https://app.codacy.com/gh/blender-for-science/blendmsh?utm_source=github.com&utm_medium=referral&utm_content=blender-for-science/blendmsh&utm_campaign=Badge_Grade_Dashboard)
[![Release](https://img.shields.io/github/v/release/blender-for-science/blendmsh)](https://github.com/blender-for-science/blendmsh/releases)
[![License](https://img.shields.io/github/license/blender-for-science/blendmsh)](https://github.com/blender-for-science/blendmsh/blob/master/LICENSE.md)

Blendmsh is a bridge between Blender 4.20+ and Gmsh, a fast and light 3D finite element mesh generator.

![Blendmsh](docs/imgs/blendmsh.png)

## Installation
![Gmsh prompt](docs/imgs/blendmshprompt.png)

*   Download the latest release as a '.zip' file and head over to Blender 4.2.0.
*   Go to **Edit->Preferences->Add-on->Install** and point to the downloaded '.zip' file.
*   Make sure that the installed add-on is enabled.
*   Once enabled, the add-on looks for Gmsh module, it prompts for an installation if Gmsh module is not found. Kindly install it either via the prompt or manually.

## Usage
### Parameters
![Parameters](docs/imgs/blendmshUI.png)

*   Workspace path
*   Physical groups
*   Element order
*   Meshing algorithm
    *   auto
    *   meshadapt
    *   del2d
    *   front2d
    *   delquad
    *   pack
    *   initial2d
    *   del3d
    *   front3d
    *   mmg3d
    *   hxt
    *   initial3d

*   Element size
*   Mesh dimension
*   Output
    *   .msh
    *   .inp
    *   .vtk

### Definition of Physical Groups
Physical groups can be defined by assigning materials to faces (Boundaries).

![Physical Groups](docs/imgs/physicalgroups.png)

### Output
Output mesh is saved to the specified workspace path, it can then be imported into FreeCAD, OpenFOAM, Paraview or anyother application that supports the above mentioned mesh format.

![Output](docs/imgs/output.png)

## Issues
Report any issues or feedback [here](https://github.com/blender-for-science/blendmsh/issues).

## References
*   [Gmsh](http://gmsh.info/doc/texinfo/gmsh.html)
*   [gmsh-api](https://pypi.org/project/gmsh-api)
