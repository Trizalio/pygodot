"""Emitter for Godot text scene files."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pygodot.dsl.values import Color, NodePath, Vec2, Vec3
from pygodot.ir.model import IRScene


@dataclass(slots=True, frozen=True)
class ExtResourceRef:
    resource_id: str


def gd_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def gd_value(value: Any) -> str:
    if isinstance(value, ExtResourceRef):
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


class TscnEmitter:
    def emit(self, scene: IRScene) -> str:
        lines: list[str] = []

        load_steps = len(scene.external_resources) + 1
        if scene.external_resources:
            lines.append(f"[gd_scene load_steps={load_steps} format=3]")
        else:
            lines.append("[gd_scene format=3]")
        lines.append("")

        for resource in scene.external_resources:
            lines.append(
                f"[ext_resource type={gd_string(resource.type)} "
                f"path={gd_string(resource.path)} "
                f"id={gd_string(resource.id)}]"
            )

        if scene.external_resources:
            lines.append("")

        self._emit_node(lines, scene.root)

        connections: list[str] = []
        self._emit_connections(connections, scene.root)
        if connections:
            lines.append("")
            lines.extend(connections)

        return "\n".join(lines).rstrip() + "\n"

    def _emit_node(self, lines: list[str], node: Any) -> None:
        if node.parent_path is None:
            lines.append(f"[node name={gd_string(node.name)} type={gd_string(node.type)}]")
        else:
            lines.append(
                f"[node name={gd_string(node.name)} "
                f"type={gd_string(node.type)} "
                f"parent={gd_string(node.parent_path)}]"
            )

        if node.script is not None:
            lines.append(f"script = {gd_value(ExtResourceRef(node.script.resource_id))}")

        for key in sorted(node.props):
            lines.append(f"{key} = {gd_value(node.props[key])}")

        lines.append("")

        for child in node.children:
            self._emit_node(lines, child)

    def _emit_connections(self, lines: list[str], node: Any) -> None:
        for conn in node.signals:
            lines.append(
                f"[connection signal={gd_string(conn.signal)} "
                f"from={gd_string(conn.from_path)} "
                f"to={gd_string(conn.target)} "
                f"method={gd_string(conn.method)}]"
            )

        for child in node.children:
            self._emit_connections(lines, child)
