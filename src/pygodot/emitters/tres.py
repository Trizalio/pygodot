"""Emitter for minimal generated Godot text resources."""

from __future__ import annotations

from pygodot.emitters.values import gd_string, gd_value
from pygodot.ir.model import IRGeneratedResource


class TresEmitter:
    def emit(self, resource: IRGeneratedResource) -> str:
        if resource.type != "LabelSettings":
            raise TypeError(f"Unsupported generated .tres resource type: {resource.type!r}.")

        lines = [f"[gd_resource type={gd_string(resource.type)} format=3]", "", "[resource]"]
        for key in sorted(resource.props):
            lines.append(f"{key} = {gd_value(resource.props[key])}")
        lines.append("")
        return "\n".join(lines)
