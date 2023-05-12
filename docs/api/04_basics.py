# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: meshwell
#     language: python
#     name: python3
# ---

# # Basics
#
# The main value of this package is the automatic tagging of complex combinations of GMSH physical entities, which allows areas of the mesh to be easily accessed for later simulation definition.

# + tags=["hide-input"]
from meshwell.mesh import mesh
import gmsh
from collections import OrderedDict

# +
# mesh?
# -

# The keys of the ordered dictionary `dimtags_dict` are associated to the corresponding values (list of entities). The values are input as a list of GMSH (dim,tag). `dim` is the dimension of the entity (0 for a 0D-point, 1 for a 1D-line, 2 for a 2D-surface, 3 for a 3D-volume). `tag` is the integer associated with the entity, which is the value returned when it is instanciated. The dimension of the returned mesh is set by the maximum `dim` across all entries.
#
# The interfaces between different entries are tagged as `{entity1_key}{interface_delimiter}{entity2_key}`, defaulting to `___`. The interface between entities and the mesh boundaries are `{entity_key}{interface_delimiter}{boundary_delimiter}`, defaulting to `None`

# Seeing this in action:

# +
gmsh.initialize()

box1 = gmsh.model.occ.addBox(0, 0, 0, 2, 2, 2)
box2 = gmsh.model.occ.addBox(1, 1, 1, 2, 2, 2)

entities = OrderedDict(
    {
        "box1": [(3, box1)],
        "box2": [(3, box2)],
    }
)

mesh_out = mesh(dimtags_dict=entities, verbosity=True, filename="mesh.msh")
# -


# Uncomment below to dynamically inspect the mesh.

# !gmsh mesh.msh

# You should see the following (toggling 3D element edges and 3D element faces):
#
# ![all](media/04_all.png)
#
# - `box1` appears earlier in the OrderedDict of entities, and hence will take precedence where it meets other entities:
#
# ![all](media/04_box1.png)
# ![all](media/04_box2.png)
#
# - Toggling 2D element edges and 2D element faces, the interface between `box1` and `box2` is rendered:
#
# ![all](media/04_box1___box2.png)
#
# - Interfaces with "nothing" (no other entities) is also rendered:
#
# ![all](media/04_box1___None.png)