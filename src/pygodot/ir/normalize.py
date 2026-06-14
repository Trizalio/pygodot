"""Normalize public DSL objects into compiler IR."""

from __future__ import annotations

from typing import Any

from pygodot.dsl.input import InputAction
from pygodot.dsl.nodes import Node
from pygodot.dsl.resources import ExternalResource
from pygodot.dsl.scene import Scene
from pygodot.dsl.settings import WindowSettings
from pygodot.dsl.script import Script
from pygodot.ir.model import (
    IRExternalResource,
    IRExternalResourceRef,
    IRInputAction,
    IRNode,
    IRPackedFloat32Array,
    IRProject,
    IRScene,
    IRScript,
    IRSignalConnection,
    IRStringName,
    IRSubResource,
    IRSubResourceRef,
    IRWindowSettings,
)
from pygodot.input_keys import normalize_key_name


def normalize_scene(scene: Scene) -> IRScene:
    resources: dict[tuple[str, str], IRExternalResource] = {}
    sub_resources: dict[str, IRSubResource] = {}
    root = _normalize_node(
        scene.root,
        node_path=".",
        parent_path=None,
        resources=resources,
        sub_resources=sub_resources,
    )
    return IRScene(
        path=scene.path,
        root=root,
        external_resources=tuple(resources[key] for key in sorted(resources)),
        sub_resources=tuple(sub_resources.values()),
    )


def normalize_project(
    *,
    name: str,
    main_scene: str,
    scenes: list[Scene],
    input_actions: list[InputAction] | None = None,
    window: WindowSettings | None = None,
) -> IRProject:
    return IRProject(
        name=name,
        main_scene=main_scene,
        scenes=tuple(normalize_scene(scene) for scene in scenes),
        input_actions=tuple(_normalize_input_action(action) for action in input_actions or []),
        window=_normalize_window(window),
    )


def _normalize_input_action(action: InputAction) -> IRInputAction:
    return IRInputAction(
        name=action.name,
        keys=tuple(normalize_key_name(key) for key in action.keys),
    )


def _normalize_window(window: WindowSettings | None) -> IRWindowSettings | None:
    if window is None:
        return None
    return IRWindowSettings(width=int(window.size.x), height=int(window.size.y))


def _normalize_node(
    node: Node,
    *,
    node_path: str,
    parent_path: str | None,
    resources: dict[tuple[str, str], IRExternalResource],
    sub_resources: dict[str, IRSubResource],
) -> IRNode:
    script = _normalize_script(node.script, resources)
    props = {key: _normalize_value(value, resources) for key, value in node.props.items()}
    props.update(_normalize_animation_libraries(node, sub_resources))
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
            sub_resources=sub_resources,
        )
        for child in node.children
    )
    return IRNode(
        name=node.name,
        type=node.type,
        path=node_path,
        parent_path=parent_path,
        props=props,
        children=children,
        script=script,
        signals=signals,
        instance=_normalize_instance(node.instance, resources),
    )


def _normalize_animation_libraries(
    node: Node,
    sub_resources: dict[str, IRSubResource],
) -> dict[str, Any]:
    if not node.animations:
        return {}

    library_data: dict[IRStringName, IRSubResourceRef] = {}
    for anim in node.animations:
        animation_id = resource_id_for_path(f"{node.name}_{anim.name}", prefix="Animation")
        track_props: dict[str, Any] = {}
        for index, track in enumerate(anim.tracks):
            track_props[f"tracks/{index}/type"] = "value"
            track_props[f"tracks/{index}/imported"] = False
            track_props[f"tracks/{index}/enabled"] = True
            track_props[f"tracks/{index}/path"] = track.path
            track_props[f"tracks/{index}/interp"] = track.interp
            track_props[f"tracks/{index}/loop_wrap"] = track.loop_wrap
            track_props[f"tracks/{index}/keys"] = {
                "times": IRPackedFloat32Array(tuple(key.time for key in track.keys)),
                "transitions": IRPackedFloat32Array(tuple(key.transition for key in track.keys)),
                "update": track.update,
                "values": [_normalize_value(key.value, {}) for key in track.keys],
            }

        sub_resources[animation_id] = IRSubResource(
            type="Animation",
            id=animation_id,
            props={
                "resource_name": anim.name,
                "length": anim.length,
                "loop_mode": 1 if anim.loop else 0,
                "step": 0.1,
                **track_props,
            },
        )
        library_data[IRStringName(anim.name)] = IRSubResourceRef(animation_id)

    library_id = resource_id_for_path(node.name, prefix="AnimationLibrary")
    sub_resources[library_id] = IRSubResource(
        type="AnimationLibrary",
        id=library_id,
        props={"_data": library_data},
    )
    return {"libraries": {IRStringName(""): IRSubResourceRef(library_id)}}


def _normalize_script(
    script: Script | None,
    resources: dict[tuple[str, str], IRExternalResource],
) -> IRScript | None:
    if script is None:
        return None

    resource = _register_external_resource(
        resources,
        ExternalResource(path=script.path, type="Script"),
    )
    return IRScript(
        path=script.path,
        extends=script.extends,
        body=script.body,
        resource_id=resource.id,
        generated=script.generated,
        source=str(script.source) if script.source is not None else None,
    )


def _normalize_value(value: Any, resources: dict[tuple[str, str], IRExternalResource]) -> Any:
    if isinstance(value, ExternalResource):
        resource = _register_external_resource(resources, value)
        return IRExternalResourceRef(resource_id=resource.id)

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


def _normalize_instance(
    value: ExternalResource | None,
    resources: dict[tuple[str, str], IRExternalResource],
) -> IRExternalResourceRef | None:
    if value is None:
        return None
    resource = _register_external_resource(resources, value)
    return IRExternalResourceRef(resource_id=resource.id)


def _register_external_resource(
    resources: dict[tuple[str, str], IRExternalResource],
    resource: ExternalResource,
) -> IRExternalResource:
    resource_id = resource_id_for_path(resource.path, prefix=resource.type)
    ir_resource = IRExternalResource(type=resource.type, path=resource.path, id=resource_id)
    resources[(resource.type, resource.path)] = ir_resource
    return ir_resource


def _child_parent_path(node: Node, parent_path: str | None) -> str:
    if parent_path is None:
        return "."
    if parent_path == ".":
        return node.name
    return f"{parent_path}/{node.name}"


def resource_id_for_path(path: str, *, prefix: str) -> str:
    safe_prefix = _safe_resource_id_part(prefix)
    safe_path = _safe_resource_id_part(path.removeprefix("res://"))
    return f"{safe_prefix}_{safe_path}"


def _safe_resource_id_part(value: str) -> str:
    return (
        value.replace("://", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(".", "_")
        .replace("-", "_")
        .replace(":", "_")
    )
