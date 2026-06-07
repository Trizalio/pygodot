"""Godot value serialization helpers."""

from __future__ import annotations

from typing import Any

from pygodot.dsl.values import Color, NodePath, Vec2, Vec3
from pygodot.ir.model import IRExternalResourceRef


def gd_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def gd_value(value: Any) -> str:
    if isinstance(value, IRExternalResourceRef):
        return f"ExtResource({gd_string(value.resource_id)})"

    if isinstance(value, str):
        return gd_string(value)

    if isinstance(value, bool):
        return "true" if value else "false"

    if value is None:
        return "null"

    if isinstance(value, int | float):
        return repr(value)

    if isinstance(value, Vec2):
        return f"Vector2({gd_value(value.x)}, {gd_value(value.y)})"

    if isinstance(value, Vec3):
        return f"Vector3({gd_value(value.x)}, {gd_value(value.y)}, {gd_value(value.z)})"

    if isinstance(value, Color):
        return f"Color({gd_value(value.r)}, {gd_value(value.g)}, {gd_value(value.b)}, {gd_value(value.a)})"

    if isinstance(value, NodePath):
        return f"NodePath({gd_string(value.path)})"

    if isinstance(value, tuple):
        if len(value) == 2:
            return f"Vector2({gd_value(value[0])}, {gd_value(value[1])})"
        if len(value) == 3:
            return f"Vector3({gd_value(value[0])}, {gd_value(value[1])}, {gd_value(value[2])})"

    if isinstance(value, list):
        return "[" + ", ".join(gd_value(item) for item in value) + "]"

    if isinstance(value, dict):
        items = ", ".join(f"{gd_value(key)}: {gd_value(item)}" for key, item in value.items())
        return "{" + items + "}"

    raise TypeError(f"Unsupported Godot value: {value!r} ({type(value).__name__})")
