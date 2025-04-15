import sys

path = sys.argv[1]
import trimesh
mesh = trimesh.load(path)
mesh.show()