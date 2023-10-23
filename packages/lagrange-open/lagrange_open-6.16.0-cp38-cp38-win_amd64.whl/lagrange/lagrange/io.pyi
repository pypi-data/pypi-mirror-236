from typing import Any, Optional, overload, Typing, Sequence
from enum import Enum
import lagrange.io

def load_mesh(filename: os.PathLike, triangulate: bool = False) -> lagrange.core.SurfaceMesh:
    """
    Load mesh from a file.
:param filename:    The input file name.
:param triangulate: Whether to triangulate the mesh if it is not already triangulated.
                    Defaults to False.
:return SurfaceMesh: The mesh object extracted from the input string.
    """
    ...

def load_simple_scene(filename: os.PathLike, triangulate: bool = False, search_path: Optional[os.PathLike] = None) -> lagrange.scene.SimpleScene3D:
    """
    Load a simple scene from file.
:param filename:    The input file name.
:param triangulate: Whether to triangulate the scene if it is not already triangulated.
                    Defaults to False.
:param search_path: Optional search path for external references (e.g. .mtl, .bin, etc.). Defaults to None.
:return SimpleScene: The scene object extracted from the input string.
    """
    ...

def mesh_to_string(mesh: lagrange.core.SurfaceMesh, format: str = 'ply', binary: bool = True, exact_match: bool = True, selected_attributes: Optional[List[int]] = None) -> bytes:
    """
    Convert a mesh to a binary string based on specified format.
:param mesh: The input mesh.
:param format: Format to use. Supported formats are "obj", "ply", "gltf" and "msh".
:param binary: Whether to save the mesh in binary format if supported. Defaults to True.
               Only `msh`, `ply` and `glb` support binary format.
:param exact_match:
               Whether to save attributes in their exact form. Some mesh formats may not support all
               the attribute types. If set to False, attributes will be converted to the closest
               supported attribute type. Defaults to True.
:param selected_attributes:
               A list of attribute ids to save. If not specified, all attributes will be saved.
               Defaults to None.
:return str: The string representing the input mesh.
    """
    ...

def save_mesh(filename: os.PathLike, mesh: lagrange.core.SurfaceMesh, binary: bool = True, exact_match: bool = True, selected_attributes: Optional[List[int]] = None) -> None:
    """
    Save mesh to file.
Filename extension determines the file format. Supported formats are: `obj`, `ply`, `msh`, `glb` and `gltf`.
:param filename: The output file name.
:param mesh: The input mesh.
:param binary: Whether to save the mesh in binary format if supported. Defaults to True.
               Only `msh`, `ply` and `glb` support binary format.
:param exact_match:
               Whether to save attributes in their exact form. Some mesh formats may not support all
               the attribute types. If set to False, attributes will be converted to the closest
               supported attribute type. Defaults to True.
:param selected_attributes:
               A list of attribute ids to save. If not specified, all attributes will be saved.
               Defaults to None.
    """
    ...

def save_simple_scene(filename: os.PathLike, scene: lagrange.scene.SimpleScene3D, binary: bool = True) -> None:
    """
    Save a simple scene to file.
:param filename: The output file name.
:param scene:    The input scene.
:param binary:   Whether to save the scene in binary format if supported. Defaults to True.
                 Only `glb` supports binary format.
    """
    ...

def string_to_mesh(data: bytes, triangulate: bool = False) -> lagrange.core.SurfaceMesh:
    """
    Convert a binary string to a mesh.
The binary string should use one of the supported formats. Supported formats include `obj`, `ply`,
`gltf`, `glb` and `msh`. Format is automatically detected.
:param data:        A binary string representing the mesh data in a supported format.
:param triangulate: Whether to triangulate the mesh if it is not already triangulated.
                    Defaults to False.
:return SurfaceMesh: The mesh object extracted from the input string.
    """
    ...

