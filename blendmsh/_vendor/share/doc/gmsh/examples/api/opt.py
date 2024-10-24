from ........ import gmsh
import sys

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " file.msh")
    exit(0)

gmsh.initialize()
try:
    gmsh.open(sys.argv[1])
except:
    exit(0)

# Second arg force optimization of discrete volumes
gmsh.model.mesh.optimize('', True)
# gmsh.model.mesh.optimize('Netgen', True)

gmsh.write('opt.msh')
gmsh.finalize()
