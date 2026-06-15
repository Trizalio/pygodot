"""Emitter for minimal generated Godot text resources."""

from __future__ import annotations

from pygodot.emitters.values import gd_string, gd_value
from pygodot.ir.model import IRGeneratedResource


class TresEmitter:
    def emit(self, resource: IRGeneratedResource) -> str:
        if resource.type != "LabelSettings":
            raise TypeError(f"Unsupported generated .tres resource type: {resource.type!r}.")

        load_steps = len(resource.external_resources) + 1
        if resource.external_resources:
            lines = [f"[gd_resource type={gd_string(resource.type)} load_steps={load_steps} format=3]", ""]
        else:
            lines = [f"[gd_resource type={gd_string(resource.type)} format=3]", ""]

        for external_resource in resource.external_resources:
            lines.append(
                f"[ext_resource type={gd_string(external_resource.type)} "
                f"path={gd_string(external_resource.path)} "
                f"id={gd_string(external_resource.id)}]"
            )

        if resource.external_resources:
            lines.append("")

        lines.append("[resource]")
        for key in sorted(resource.props):
            lines.append(f"{key} = {gd_value(resource.props[key])}")
        lines.append("")
        return "\n".join(lines)
