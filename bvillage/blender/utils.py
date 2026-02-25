# bvillage/blender/utils.py

from __future__ import annotations
import bpy


def ensure_collection(name: str, parent: bpy.types.Collection | None = None) -> bpy.types.Collection:
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
    if parent is None:
        if col.name not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(col)
    else:
        if col.name not in parent.children:
            parent.children.link(col)
    return col


def clear_collection(col: bpy.types.Collection):
    # Unlink and delete objects in collection (safe-ish for generated stuff)
    objs = list(col.objects)
    for o in objs:
        col.objects.unlink(o)
        bpy.data.objects.remove(o, do_unlink=True)


def link_object(obj: bpy.types.Object, col: bpy.types.Collection):
    if obj.name not in col.objects:
        col.objects.link(obj)


def new_empty(name: str) -> bpy.types.Object:
    o = bpy.data.objects.new(name, None)
    o.empty_display_type = "PLAIN_AXES"
    o.empty_display_size = 0.2
    return o
