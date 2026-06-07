"""Validation for normalized IR."""

from typing import Any

from pygodot.emitters.values import gd_value
from pygodot.errors import ValidationError
from pygodot.ir.model import IRNode, IRProject, IRScene


def validate_project(project: IRProject) -> None:
    if not project.name:
        raise ValidationError("Project name must not be empty.")
    if not _is_res_path(project.main_scene):
        raise ValidationError(f"Main scene path must start with res://, got {project.main_scene!r}.")
    if not project.scenes:
        raise ValidationError("Game must contain at least one scene.")
    scene_paths = {scene.path for scene in project.scenes}
    if project.main_scene not in scene_paths:
        raise ValidationError(f"Main scene {project.main_scene!r} is not registered in the game.")
    for scene in project.scenes:
        validate_scene(scene)


def validate_scene(scene: IRScene) -> None:
    if not _is_res_path(scene.path):
        raise ValidationError(f"Scene path must start with res://, got {scene.path!r}.")
    _validate_node(scene.root, scene_path=scene.path)
    for resource in scene.external_resources:
        if not resource.type:
            raise ValidationError(f"External resource type must not be empty for {resource.path!r}.")
        if not _is_res_path(resource.path):
            raise ValidationError(f"External resource path must start with res://, got {resource.path!r}.")
        if not resource.id:
            raise ValidationError(f"External resource id must not be empty for {resource.path!r}.")


def _validate_node(node: IRNode, *, scene_path: str) -> None:
    location = f"{scene_path}:{node.path}"
    if not node.name:
        raise ValidationError(f"Node name must not be empty at {location}.")
    if "/" in node.name:
        raise ValidationError(f"Node name must not contain '/' at {location}: {node.name!r}.")
    if not node.type:
        raise ValidationError(f"Node type must not be empty at {location}.")
    if node.script is not None:
        if not _is_res_path(node.script.path):
            raise ValidationError(f"Script path must start with res:// at {location}: {node.script.path!r}.")
        if not node.script.extends:
            raise ValidationError(f"Script extends must not be empty at {location}.")
    for key, value in node.props.items():
        _validate_supported_value(value, property_name=key, location=location)
    for conn in node.signals:
        if not conn.signal:
            raise ValidationError(f"Signal name must not be empty at {location}.")
        if not conn.target:
            raise ValidationError(f"Signal target must not be empty at {location}.")
        if not conn.method:
            raise ValidationError(f"Signal method must not be empty at {location}.")

    seen: set[str] = set()
    for child in node.children:
        if child.name in seen:
            raise ValidationError(f"Duplicate child node name {child.name!r} under {location}.")
        seen.add(child.name)
        _validate_node(child, scene_path=scene_path)


def _validate_supported_value(value: Any, *, property_name: str, location: str) -> None:
    try:
        gd_value(value)
    except TypeError as exc:
        raise ValidationError(
            f"Unsupported value for property {property_name!r} at {location}: {value!r}."
        ) from exc


def _is_res_path(path: str) -> bool:
    return path.startswith("res://")
