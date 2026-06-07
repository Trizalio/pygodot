"""Emitter for Godot text scene files."""

from __future__ import annotations

from typing import Any

from pygodot.emitters.values import gd_string, gd_value
from pygodot.ir.model import IRExternalResourceRef
from pygodot.ir.model import IRScene


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
            lines.append(f"script = {gd_value(IRExternalResourceRef(node.script.resource_id))}")

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
