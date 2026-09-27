"""Minimal Blender scene validator for Assetto Corsa map source scenes.

Run inside Blender's Scripting workspace or with:
    blender your_scene.blend --background --python examples/blender/validate_scene.py

This script intentionally performs conservative source-scene checks. It does not
claim to validate KN5 serialization or every ksEditor requirement.
"""

import re

import bpy


SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
errors = []
warnings = []

mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]

for obj in mesh_objects:
    if " " in obj.name or not SAFE_NAME.match(obj.name):
        warnings.append(f"{obj.name}: consider using export-safe ASCII naming")

    if obj.scale != obj.scale.__class__((1.0, 1.0, 1.0)):
        warnings.append(f"{obj.name}: unapplied scale {tuple(round(v, 5) for v in obj.scale)}")

    if len(obj.data.polygons) == 0:
        errors.append(f"{obj.name}: mesh has no faces")

    if len(obj.data.uv_layers) == 0:
        warnings.append(f"{obj.name}: mesh has no UV map")

    if len(obj.material_slots) == 0:
        warnings.append(f"{obj.name}: mesh has no material slots")

print("=== Assetto Map Tools: Blender validation ===")
print(f"Mesh objects: {len(mesh_objects)}")
for item in errors:
    print(f"ERROR: {item}")
for item in warnings:
    print(f"WARN:  {item}")
print(f"Result: {len(errors)} error(s), {len(warnings)} warning(s)")

if errors:
    raise SystemExit(1)
