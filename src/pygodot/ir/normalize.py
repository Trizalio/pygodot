"""Normalize public DSL objects into compiler IR."""

from __future__ import annotations

from typing import Any

from pygodot.dsl.nodes import Node
from pygodot.dsl.resources import ExternalResource
from pygodot.dsl.scene import Scene
from pygodot.dsl.script import Script
from pygodot.ir.model import (
    IRExternalResource,
    IRExternalResourceRef,
    IRNode,
    IRProject,
    IRScene,
    IRScript,
    IRSignalConnection,
)


def normalize_scene(scene: Scene) -> IRScene:
    resources: dict[str, IRExternalResource] = {}
    root = _normalize_node(
        scene.root,
        node_path=".",
        parent_path=None,
        resources=resources,
    )
    return IRScene(
        path=scene.path,
        root=root,
        external_resources=tuple(resources[path] for path in sorted(resources)),
    )


def normalize_project(*, name: str, main_scene: str, scenes: list[Scene]) -> IRProject:
    return IRProject(
        name=name,
        main_scene=main_scene,
        scenes=tuple(normalize_scene(scene) for scene in scenes),
    )


def _normalize_node(
    node: Node,
    *,
    node_path: str,
    parent_path: str | None,
    resources: dict[str, IRExternalResource],
) -> IRNode:
    script = _normalize_script(node.script, resources)
    signals = tuple(
        IRSignalConnection(
            signal=conn.signal,
            from_path=node_path,
            target=conn.target,
            method=conn.method,
        )
        for conn in node.signals
    )
    children = tuple(
        _normalize_node(
            child,
            node_path=child.name if node_path == "." else f"{node_path}/{child.name}",
            parent_path=_child_parent_path(node, parent_path),
            resources=resources,
        )
        for child in node.children
    )
    return IRNode(
        name=node.name,
        type=node.type,
        path=node_path,
        parent_path=parent_path,
        props={key: _normalize_value(value, resources) for key, value in node.props.items()},
        children=children,
        script=script,
        signals=signals,
    )


def _normalize_script(
    script: Script | None,
    resources: dict[str, IRExternalResource],
) -> IRScript | None:
    if script is None:
        return None

    resource_id = resource_id_for_path(script.path, prefix="Script")
    resources[script.path] = IRExternalResource(type="Script", path=script.path, id=resource_id)
    return IRScript(
        path=script.path,
        extends=script.extends,
        body=script.body,
        resource_id=resource_id,
    )


def _normalize_value(value: Any, resources: dict[str, IRExternalResource]) -> Any:
    if isinstance(value, ExternalResource):
        resource_id = resource_id_for_path(value.path, prefix=value.type)
        resources[value.path] = IRExternalResource(type=value.type, path=value.path, id=resource_id)
        return IRExternalResourceRef(resource_id=resource_id)

    if isinstance(value, list):
        return [_normalize_value(item, resources) for item in value]

    if isinstance(value, tuple):
        return tuple(_normalize_value(item, resources) for item in value)

    if isinstance(value, dict):
        return {
            _normalize_value(key, resources): _normalize_value(item, resources)
            for key, item in value.items()
        }

    return value


def _child_parent_path(node: Node, parent_path: str | None) -> str:
    if parent_path is None:
        return "."
    if parent_path == ".":
        return node.name
    return f"{parent_path}/{node.name}"


def resource_id_for_path(path: str, *, prefix: str) -> str:
    safe = path.removeprefix("res://").replace("/", "_").replace(".", "_").replace("-", "_")
    return f"{prefix}_{safe}"
