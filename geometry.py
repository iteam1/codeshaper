import numpy as np
import trimesh

def make_cube(size=1.0):
    return trimesh.creation.box(extents=(size, size, size))

def make_sphere(radius=1.0):
    return trimesh.creation.icosphere(radius=radius)

def apply_transform(mesh, translation=None):
    if translation:
        mesh.apply_translation(translation)
    return mesh
