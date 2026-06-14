"""Normalize public DSL objects into compiler IR."""

from __future__ import annotations

from typing import Any

from pygodot.dsl.generated_resources import GeneratedResource
from pygodot.dsl.input import InputAction
from pygodot.dsl.nodes import Node
from pygodot.dsl.resources import ExternalResource
from pygodot.dsl.scene import Scene
from pygodot.dsl.settings import WindowSettings
from pygodot.dsl.shapes import CircleShape2D, RectangleShape2D
from pygodot.dsl.script import Script
from pygodot.dsl.subresources import SubResource
from pygodot.ir.model import (
    IRExternalResource,
    IRExternalResourceRef,
    IRGeneratedResource,
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


def normalize_scene(
    scene: Scene,
    generated_resources: dict[tuple[str, str], IRGeneratedResource] | None = None,
) -> IRScene:
    resources: dict[tuple[str, str], IRExternalResource] = {}
    sub_resources: dict[str, IRSubResource] = {}
    generated_resources = generated_resources if generated_resources is not None else {}
    root = _normalize_node(
        scene.root,
        node_path=".",
        parent_path=None,
        resources=resources,
        sub_resources=sub_resources,
        generated_resources=generated_resources,
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
    generated_resources: dict[tuple[str, str], IRGeneratedResource] = {}
    return IRProject(
        name=name,
        main_scene=main_scene,
        scenes=tuple(normalize_scene(scene, generated_resources) for scene in scenes),
        generated_resources=tuple(generated_resources[key] for key in sorted(generated_resources)),
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
    generated_resources: dict[tuple[str, str], IRGeneratedResource],
) -> IRNode:
    script = _normalize_script(node.script, resources)
    props = {
        key: _normalize_value(value, resources, sub_resources, generated_resources)
        for key, value in node.props.items()
    }
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
            generated_resources=generated_resources,
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
        template_context=script.template_context,
    )


def _normalize_value(
    value: Any,
    resources: dict[tuple[str, str], IRExternalResource],
    sub_resources: dict[str, IRSubResource] | None = None,
    generated_resources: dict[tuple[str, str], IRGeneratedResource] | None = None,
) -> Any:
    if isinstance(value, GeneratedResource):
        if generated_resources is None:
            raise TypeError("Generated resources require a project generated resource registry.")
        resource = _register_generated_resource(resources, generated_resources, value)
        return IRExternalResourceRef(resource_id=resource.id)

    if isinstance(value, ExternalResource):
        resource = _register_external_resource(resources, value)
        return IRExternalResourceRef(resource_id=resource.id)

    sub_resource_value = _as_sub_resource(value)
    if sub_resource_value is not None:
        if sub_resources is None:
            raise TypeError("Sub-resources require a scene sub-resource registry.")
        return _register_sub_resource(resources, sub_resources, sub_resource_value)

    if isinstance(value, list):
        return [_normalize_value(item, resources, sub_resources, generated_resources) for item in value]

    if isinstance(value, tuple):
        return tuple(_normalize_value(item, resources, sub_resources, generated_resources) for item in value)

    if isinstance(value, dict):
        return {
            _normalize_value(key, resources, sub_resources, generated_resources): _normalize_value(
                item,
                resources,
                sub_resources,
                generated_resources,
            )
            for key, item in value.items()
        }

    return value


def _as_sub_resource(value: Any) -> SubResource | None:
    if isinstance(value, SubResource):
        return value
    if isinstance(value, (RectangleShape2D, CircleShape2D)):
        return value.as_sub_resource()
    return None


def _register_sub_resource(
    resources: dict[tuple[str, str], IRExternalResource],
    sub_resources: dict[str, IRSubResource],
    resource: SubResource,
) -> IRSubResourceRef:
    resource_id = resource_id_for_path(
        resource.id_hint,
        prefix=resource.type,
    )
    sub_resources.setdefault(
        resource_id,
        IRSubResource(
            type=resource.type,
            id=resource_id,
            props={
                key: _normalize_value(value, resources, sub_resources)
                for key, value in resource.props.items()
            },
        ),
    )
    return IRSubResourceRef(resource_id)


def _register_generated_resource(
    resources: dict[tuple[str, str], IRExternalResource],
    generated_resources: dict[tuple[str, str], IRGeneratedResource],
    resource: GeneratedResource,
) -> IRExternalResource:
    external_resource = _register_external_resource(
        resources,
        ExternalResource(path=resource.path, type=resource.type),
    )
    ir_resource = IRGeneratedResource(
        type=resource.type,
        path=resource.path,
        id=external_resource.id,
        props={
            key: _normalize_value(value, resources, None, generated_resources)
            for key, value in resource.props.items()
        },
    )
    key = (resource.type, resource.path)
    existing = generated_resources.get(key)
    if existing is not None and existing != ir_resource:
        raise ValueError(
            f"Generated resource declared more than once with different properties: "
            f"type={resource.type!r}, path={resource.path!r}."
        )
    generated_resources[key] = ir_resource
    return external_resource


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
