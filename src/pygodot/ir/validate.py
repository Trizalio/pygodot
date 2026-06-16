"""Validation for normalized IR."""

from typing import Any

from pygodot.emitters.values import gd_value
from pygodot.errors import ValidationError
from pygodot.input_keys import keycode_for
from pygodot.input_mouse import mouse_button_index_for
from pygodot.ir.generated_resources import supported_generated_resource_types
from pygodot.ir.model import (
    IRExternalResource,
    IRGeneratedResource,
    IRAutoload,
    IRInputAction,
    IRNode,
    IRProject,
    IRProjectSetting,
    IRScene,
    IRSubResource,
    IRWindowSettings,
)


def validate_project(project: IRProject) -> None:
    if not project.name:
        raise ValidationError("Project name must not be empty.")
    if not _is_res_path(project.main_scene):
        raise ValidationError(
            f"Main scene path must start with res://: main_scene={project.main_scene!r}."
        )
    if not project.scenes:
        raise ValidationError("Game must contain at least one scene.")
    scene_paths = {scene.path for scene in project.scenes}
    if project.main_scene not in scene_paths:
        raise ValidationError(
            f"Main scene is not registered in the game: "
            f"main_scene={project.main_scene!r}, registered_scenes={sorted(scene_paths)!r}."
        )
    for scene in project.scenes:
        validate_scene(scene)
    for resource in project.generated_resources:
        _validate_generated_resource(resource)
    _validate_autoloads(project.autoloads)
    if project.icon is not None:
        _validate_external_resource(project.icon, location="project icon")
    _validate_project_settings(project.project_settings)
    _validate_input_actions(project.input_actions)
    _validate_window(project.window)


def validate_scene(scene: IRScene) -> None:
    if not _is_res_path(scene.path):
        raise ValidationError(f"Scene path must start with res://: scene={scene.path!r}.")
    _validate_node(scene.root, scene_path=scene.path)
    for resource in scene.external_resources:
        _validate_external_resource(resource, location=f"scene={scene.path!r}")
    for resource in scene.sub_resources:
        _validate_sub_resource(resource, scene_path=scene.path)


def _validate_sub_resource(resource: IRSubResource, *, scene_path: str) -> None:
    if not resource.type:
        raise ValidationError(
            f"Sub-resource type must not be empty: scene={scene_path!r}, "
            f"resource_id={resource.id!r}."
        )
    if not resource.id:
        raise ValidationError(
            f"Sub-resource id must not be empty: scene={scene_path!r}, "
            f"resource_type={resource.type!r}."
        )
    for key, value in resource.props.items():
        _validate_supported_value(
            value,
            value_path=f"sub-resource {resource.id!r} property {key!r}",
            location=f"scene={scene_path!r}",
        )


def _validate_generated_resource(resource: IRGeneratedResource) -> None:
    if resource.type not in supported_generated_resource_types():
        raise ValidationError(
            f"Unsupported generated resource type: "
            f"resource_path={resource.path!r}, resource_type={resource.type!r}."
        )
    if not _is_res_path(resource.path):
        raise ValidationError(
            f"Generated resource path must start with res://: "
            f"resource_type={resource.type!r}, resource_path={resource.path!r}."
        )
    if not resource.id:
        raise ValidationError(
            f"Generated resource id must not be empty: "
            f"resource_type={resource.type!r}, resource_path={resource.path!r}."
        )
    for key, value in resource.props.items():
        _validate_supported_value(
            value,
            value_path=f"generated resource {resource.path!r} property {key!r}",
            location=f"resource_type={resource.type!r}",
        )
    for external_resource in resource.external_resources:
        _validate_external_resource(
            external_resource,
            location=f"generated_resource={resource.path!r}",
        )


def _validate_external_resource(resource: IRExternalResource, *, location: str) -> None:
    if not resource.type:
        raise ValidationError(
            f"External resource type must not be empty: {location}, "
            f"resource_path={resource.path!r}, resource_id={resource.id!r}."
        )
    if not _is_res_path(resource.path):
        raise ValidationError(
            f"External resource path must start with res://: {location}, "
            f"resource_type={resource.type!r}, resource_path={resource.path!r}."
        )
    if not resource.id:
        raise ValidationError(
            f"External resource id must not be empty: {location}, "
            f"resource_type={resource.type!r}, resource_path={resource.path!r}."
        )


def _validate_node(node: IRNode, *, scene_path: str) -> None:
    location = _location(scene_path, node.path)
    if not node.name:
        raise ValidationError(f"Node name must not be empty: {location}.")
    if "/" in node.name:
        raise ValidationError(
            f"Node name must not contain '/': {location}, node_name={node.name!r}."
        )
    if not node.type and node.instance is None:
        raise ValidationError(f"Node type must not be empty: {location}.")
    if node.script is not None:
        if not _is_res_path(node.script.path):
            raise ValidationError(
                f"Script path must start with res://: {location}, script_path={node.script.path!r}."
            )
        if not node.script.extends:
            raise ValidationError(
                f"Script extends must not be empty: {location}, script_path={node.script.path!r}."
            )
        if node.script.generated and node.script.source is not None and node.script.body.strip():
            raise ValidationError(
                f"Generated script must use either body or source, not both: "
                f"{location}, script_path={node.script.path!r}."
            )
        if node.script.generated and node.script.source is None and not node.script.body.strip():
            raise ValidationError(
                f"Generated script body must not be empty: {location}, script_path={node.script.path!r}."
            )
        if not node.script.generated and (
            node.script.body.strip()
            or node.script.source is not None
            or node.script.template_context is not None
        ):
            raise ValidationError(
                f"Referenced manual script must not define generated content: "
                f"{location}, script_path={node.script.path!r}."
            )
    for key, value in node.props.items():
        _validate_supported_value(value, value_path=f"property {key!r}", location=location)
    for conn in node.signals:
        if not conn.signal:
            raise ValidationError(f"Signal name must not be empty: {location}, method={conn.method!r}.")
        if not conn.target:
            raise ValidationError(
                f"Signal target must not be empty: {location}, "
                f"signal={conn.signal!r}, method={conn.method!r}."
            )
        if not conn.method:
            raise ValidationError(
                f"Signal method must not be empty: {location}, signal={conn.signal!r}, target={conn.target!r}."
            )

    seen: set[str] = set()
    for child in node.children:
        if child.name in seen:
            raise ValidationError(
                f"Duplicate child node name: {location}, child_name={child.name!r}."
            )
        seen.add(child.name)
        _validate_node(child, scene_path=scene_path)


def _validate_supported_value(value: Any, *, value_path: str, location: str) -> None:
    try:
        gd_value(value)
    except TypeError as exc:
        raise ValidationError(
            f"Unsupported value for {value_path}: {location}, "
            f"value={value!r}, value_type={type(value).__name__}."
        ) from exc


def _validate_input_actions(actions: tuple[IRInputAction, ...]) -> None:
    seen: set[str] = set()
    for action in actions:
        if not _is_valid_input_action_name(action.name):
            raise ValidationError(
                f"Input action name must contain only letters, numbers, and underscores: "
                f"action={action.name!r}."
            )
        if action.name in seen:
            raise ValidationError(f"Duplicate input action name: action={action.name!r}.")
        seen.add(action.name)
        if not action.keys and not action.mouse_buttons:
            raise ValidationError(
                f"Input action must contain at least one key or mouse button: action={action.name!r}."
            )
        for key in action.keys:
            if keycode_for(key) is None:
                raise ValidationError(
                    f"Unsupported input action key: action={action.name!r}, key={key!r}."
                )
        for button in action.mouse_buttons:
            if mouse_button_index_for(button) is None:
                raise ValidationError(
                    f"Unsupported input action mouse button: action={action.name!r}, "
                    f"mouse_button={button!r}."
                )


def _is_valid_input_action_name(name: str) -> bool:
    if not name:
        return False
    return all(char.isalnum() or char == "_" for char in name)


def _validate_autoloads(autoloads: tuple[IRAutoload, ...]) -> None:
    seen: set[str] = set()
    for autoload in autoloads:
        if not _is_valid_autoload_name(autoload.name):
            raise ValidationError(
                f"Autoload name must contain only letters, numbers, and underscores: "
                f"autoload={autoload.name!r}."
            )
        if autoload.name in seen:
            raise ValidationError(f"Duplicate autoload name: autoload={autoload.name!r}.")
        seen.add(autoload.name)
        if not _is_safe_res_path(autoload.path):
            raise ValidationError(
                f"Autoload path must be a safe res:// path: "
                f"autoload={autoload.name!r}, path={autoload.path!r}."
            )


def _is_valid_autoload_name(name: str) -> bool:
    if not name:
        return False
    if not (name[0].isalpha() or name[0] == "_"):
        return False
    return all(char.isalnum() or char == "_" for char in name)


def _validate_project_settings(settings: tuple[IRProjectSetting, ...]) -> None:
    seen: set[str] = set()
    for setting in settings:
        if not _is_valid_project_setting_path(setting.path):
            raise ValidationError(f"Invalid project setting path: path={setting.path!r}.")
        if setting.path in seen:
            raise ValidationError(f"Duplicate project setting path: path={setting.path!r}.")
        seen.add(setting.path)
        try:
            gd_value(setting.value)
        except TypeError as exc:
            raise ValidationError(
                f"Unsupported project setting value: path={setting.path!r}, "
                f"value={setting.value!r}, value_type={type(setting.value).__name__}."
            ) from exc


def _is_valid_project_setting_path(path: str) -> bool:
    if not path or "/" not in path:
        return False
    if path.startswith("/") or path.endswith("/"):
        return False
    return all(part for part in path.split("/"))


def _validate_window(window: IRWindowSettings | None) -> None:
    if window is None:
        return
    if window.width <= 0 or window.height <= 0:
        raise ValidationError(
            f"Window size must be positive: width={window.width!r}, height={window.height!r}."
        )
    if window.stretch_mode is not None and not window.stretch_mode:
        raise ValidationError("Window stretch mode must not be empty.")
    if window.stretch_aspect is not None and not window.stretch_aspect:
        raise ValidationError("Window stretch aspect must not be empty.")


def _location(scene_path: str, node_path: str) -> str:
    return f"scene={scene_path!r}, node={node_path!r}"


def _is_res_path(path: str) -> bool:
    return path.startswith("res://")


def _is_safe_res_path(path: str) -> bool:
    if not _is_res_path(path):
        return False
    relative = path.removeprefix("res://")
    if not relative:
        return False
    return ".." not in relative.replace("\\", "/").split("/")
