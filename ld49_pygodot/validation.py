from __future__ import annotations

import json
from pathlib import Path

REQUIRED_GENERATED_FILES = {
    ".pygodot/manifest.json",
    "project.godot",
    "scenes/end.tscn",
    "scenes/fader.tscn",
    "scenes/intro.tscn",
    "scenes/main.tscn",
    "scenes/spell.tscn",
    "scenes/tile.tscn",
    "scenes/unit.tscn",
    "scripts/end.gd",
    "scripts/fader.gd",
    "scripts/intro.gd",
    "scripts/main.gd",
    "scripts/spell.gd",
    "scripts/tile.gd",
    "scripts/unit.gd",
}

REQUIRED_COPIED_FILES = {
    "resources/icon.svg",
    "scripts/audio_manager.gd",
    "scripts/game_state.gd",
    "scripts/matrix.gd",
    "scripts/matrix_utils.gd",
    "scripts/rand.gd",
    "scripts/scene_changer.gd",
    "scripts/utils.gd",
}

REQUIRED_AUTOLOADS = {
    "Matrix": "res://scripts/matrix.gd",
    "MatrixUtils": "res://scripts/matrix_utils.gd",
    "Rand": "res://scripts/rand.gd",
    "Utils": "res://scripts/utils.gd",
    "GameState": "res://scripts/game_state.gd",
    "SceneChanger": "res://scripts/scene_changer.gd",
    "AudioManager": "res://scripts/audio_manager.gd",
}

REQUIRED_SCENE_MARKERS = {
    "scenes/main.tscn": [
        'instance=ExtResource("PackedScene_scenes_tile_tscn")',
        'instance=ExtResource("PackedScene_scenes_spell_tscn")',
        "Castle 0/6 D:0 U:0 G:0",
        "Pass Turn",
    ],
    "scenes/end.tscn": ["Battle Complete", "stage_f"],
    "scenes/spell.tscn": ["Script_scripts_spell_gd"],
    "scenes/tile.tscn": ["Script_scripts_tile_gd"],
    "scenes/unit.tscn": ["Script_scripts_unit_gd"],
}


def validate_build(project_dir: Path) -> list[str]:
    project_dir = Path(project_dir)
    issues: list[str] = []

    _require_files(project_dir, REQUIRED_GENERATED_FILES | REQUIRED_COPIED_FILES, issues)

    manifest_path = project_dir / ".pygodot" / "manifest.json"
    manifest = _read_manifest(manifest_path, issues)
    if manifest is not None:
        _validate_manifest(manifest, issues)

    project_text = _read_text(project_dir / "project.godot", issues)
    if project_text is not None:
        if 'run/main_scene="res://scenes/main.tscn"' not in project_text:
            issues.append("project.godot does not point at res://scenes/main.tscn")
        for name, path in REQUIRED_AUTOLOADS.items():
            if f'{name}="*{path}"' not in project_text:
                issues.append(f"project.godot is missing autoload {name} -> {path}")

    for relative_path, markers in REQUIRED_SCENE_MARKERS.items():
        text = _read_text(project_dir / relative_path, issues)
        if text is None:
            continue
        for marker in markers:
            if marker not in text:
                issues.append(f"{relative_path} is missing marker: {marker}")

    return issues


def _require_files(project_dir: Path, relative_paths: set[str], issues: list[str]) -> None:
    for relative_path in sorted(relative_paths):
        if not (project_dir / relative_path).is_file():
            issues.append(f"missing required file: {relative_path}")


def _read_manifest(path: Path, issues: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append("missing required file: .pygodot/manifest.json")
    except json.JSONDecodeError as exc:
        issues.append(f".pygodot/manifest.json is not valid JSON: {exc}")
    return None


def _read_text(path: Path, issues: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(f"missing required file: {path.as_posix()}")
    return None


def _validate_manifest(manifest: dict, issues: list[str]) -> None:
    generated_files = set(manifest.get("generated_files", []))
    missing_generated = REQUIRED_GENERATED_FILES - generated_files
    if missing_generated:
        issues.append(f"manifest missing generated files: {sorted(missing_generated)}")

    resources_by_path = {
        resource.get("path"): resource
        for resource in manifest.get("external_resources", [])
    }
    for path in [
        "res://scenes/spell.tscn",
        "res://scenes/tile.tscn",
    ]:
        resource = resources_by_path.get(path)
        if resource is None:
            issues.append(f"manifest missing PackedScene resource: {path}")
        elif resource.get("ownership") != "generated":
            issues.append(f"manifest resource {path} should be generated")

    for path in [
        "res://scripts/audio_manager.gd",
        "res://scripts/game_state.gd",
        "res://scripts/matrix.gd",
        "res://scripts/matrix_utils.gd",
        "res://scripts/rand.gd",
        "res://scripts/scene_changer.gd",
        "res://scripts/utils.gd",
    ]:
        resource = resources_by_path.get(path)
        if resource is None:
            issues.append(f"manifest missing copied script resource: {path}")
        elif resource.get("ownership") != "copied":
            issues.append(f"manifest resource {path} should be copied")
