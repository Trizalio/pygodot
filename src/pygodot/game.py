"""Library-first game orchestration API."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from pygodot.build.manifest import BuildManifest, ManifestResource
from pygodot.build.writer import GeneratedFileWriter
from pygodot.dsl.input import InputAction
from pygodot.dsl.scene import Scene
from pygodot.dsl.settings import WindowSettings
from pygodot.dsl.values import Vec2
from pygodot.errors import BuildError
from pygodot.emitters.gdscript import GdScriptEmitter
from pygodot.emitters.project import ProjectEmitter
from pygodot.emitters.tscn import TscnEmitter
from pygodot.godot_cli import GodotRunResult, check_project_run, import_project, run_project
from pygodot.ir.model import IRExternalResource, IRNode, IRProject, IRScript
from pygodot.ir.normalize import normalize_project
from pygodot.ir.validate import validate_project


@dataclass(slots=True, frozen=True)
class BuildResult:
    """Structured result returned by Game.build()."""

    project_dir: Path
    written_files: list[Path]
    generated_scenes: list[Path]
    generated_scripts: list[Path]
    copied_resources: list[Path] = field(default_factory=list)
    manifest_path: Path | None = None


@dataclass(slots=True)
class Game:
    """A user-owned Godot project declaration."""

    name: str
    source_root: Path
    build_dir: Path
    main_scene: str
    godot_bin: str = "godot"
    scenes: list[Scene] = field(default_factory=list)
    input_actions: list[InputAction] = field(default_factory=list)
    window: WindowSettings | None = None

    def add_scene(self, scene: Scene) -> None:
        self.scenes.append(scene)

    def add_input_action(self, name: str, *, keys: list[str]) -> None:
        self.input_actions.append(InputAction(name=name, keys=tuple(keys)))

    def set_window(self, *, size: Vec2) -> None:
        self.window = WindowSettings(size=size)

    def build(self) -> BuildResult:
        project = normalize_project(
            name=self.name,
            main_scene=self.main_scene,
            scenes=self.scenes,
            input_actions=self.input_actions,
            window=self.window,
        )
        validate_project(project)

        writer = GeneratedFileWriter(self.build_dir, allow_overwrite_unmarked=True)
        project_emitter = ProjectEmitter()
        scene_emitter = TscnEmitter()
        script_emitter = GdScriptEmitter()

        written_files: list[Path] = []
        generated_scenes: list[Path] = []
        generated_scripts: list[Path] = []
        copied_resources: list[Path] = []
        manifest = BuildManifest()

        project_file = writer.write_text(Path("project.godot"), project_emitter.emit(project))
        written_files.append(project_file)
        manifest.generated_files.append(_rel_to_project(self.build_dir, project_file))

        emitted_script_paths: set[str] = set()
        for scene in project.scenes:
            for script in _iter_scripts(scene.root):
                if not script.generated:
                    continue
                if script.path in emitted_script_paths:
                    continue
                emitted_script_paths.add(script.path)
                script_path = writer.write_text(
                    _res_to_rel(script.path),
                    script_emitter.emit(_resolve_generated_script(script, self.source_root)),
                )
                written_files.append(script_path)
                generated_scripts.append(script_path)
                rel_script_path = _rel_to_project(self.build_dir, script_path)
                manifest.generated_files.append(rel_script_path)
                manifest.generated_scripts.append(rel_script_path)

            scene_path = writer.write_text(_res_to_rel(scene.path), scene_emitter.emit(scene))
            written_files.append(scene_path)
            generated_scenes.append(scene_path)
            rel_scene_path = _rel_to_project(self.build_dir, scene_path)
            manifest.generated_files.append(rel_scene_path)
            manifest.generated_scenes.append(rel_scene_path)

        copied_resources.extend(_copy_external_resources(project, writer, self.source_root, manifest))
        manifest_relative_path = Path(".pygodot") / "manifest.json"
        manifest.generated_files.append(manifest_relative_path.as_posix())
        manifest_path = writer.write_text(
            manifest_relative_path,
            manifest.to_json(),
            mark_generated=False,
        )
        written_files.append(manifest_path)

        return BuildResult(
            project_dir=self.build_dir,
            written_files=written_files,
            generated_scenes=generated_scenes,
            generated_scripts=generated_scripts,
            copied_resources=copied_resources,
            manifest_path=manifest_path,
        )

    def run(self, scene: str | None = None) -> None:
        result = self.build()
        import_project(result.project_dir, godot_bin=self.godot_bin)
        run_project(result.project_dir, godot_bin=self.godot_bin, scene=scene or self.main_scene)

    def check_run(self, *, scene: str | None = None, frames: int = 20) -> GodotRunResult:
        result = self.build()
        import_project(result.project_dir, godot_bin=self.godot_bin)
        return check_project_run(
            result.project_dir,
            godot_bin=self.godot_bin,
            scene=scene or self.main_scene,
            frames=frames,
        )


def _iter_scripts(node: IRNode) -> list[IRScript]:
    scripts: list[IRScript] = []
    if node.script is not None:
        scripts.append(node.script)
    for child in node.children:
        scripts.extend(_iter_scripts(child))
    return scripts


def _resolve_generated_script(script: IRScript, source_root: Path) -> IRScript:
    if script.source is None:
        return script

    source_path = _source_to_rel(script.source)
    absolute_source = source_root / source_path
    if not absolute_source.is_file():
        raise BuildError(
            f"Generated script source file does not exist: "
            f"script_path={script.path!r}, source={script.source!r}."
        )

    body = absolute_source.read_text(encoding="utf-8")
    if not body.strip():
        raise BuildError(
            f"Generated script source must not be empty: "
            f"script_path={script.path!r}, source={script.source!r}."
        )

    return IRScript(
        path=script.path,
        extends=script.extends,
        body=body,
        resource_id=script.resource_id,
        generated=script.generated,
        source=script.source,
    )


def _copy_external_resources(
    project: IRProject,
    writer: GeneratedFileWriter,
    source_root: Path,
    manifest: BuildManifest,
) -> list[Path]:
    copied: list[Path] = []
    seen: set[tuple[str, str]] = set()
    for resource in _iter_external_resources(project):
        key = (resource.type, resource.path)
        if key in seen:
            continue
        seen.add(key)

        if resource.type == "Script":
            manifest.external_resources.append(
                ManifestResource(
                    type=resource.type,
                    path=resource.path,
                    id=resource.id,
                    copied=False,
                )
            )
            continue

        relative_path = _res_to_rel(resource.path)
        source = source_root / relative_path
        copied_path: Path | None = None
        if source.is_file():
            copied_path = writer.copy_file(source, relative_path)
            copied.append(copied_path)

        manifest.external_resources.append(
            ManifestResource(
                type=resource.type,
                path=resource.path,
                id=resource.id,
                copied=copied_path is not None,
            )
        )
    return copied


def _iter_external_resources(project: IRProject) -> list[IRExternalResource]:
    resources: list[IRExternalResource] = []
    for scene in project.scenes:
        resources.extend(scene.external_resources)
    return resources


def _rel_to_project(project_dir: Path, path: Path) -> str:
    return path.relative_to(project_dir).as_posix()


def _res_to_rel(path: str) -> Path:
    if not path.startswith("res://"):
        raise BuildError(f"Expected res:// path, got {path!r}.")
    relative = Path(path.removeprefix("res://"))
    if relative.is_absolute() or ".." in relative.parts:
        raise BuildError(f"Unsafe res:// path cannot leave project root: path={path!r}.")
    if not relative.parts:
        raise BuildError(f"Expected non-empty res:// path, got {path!r}.")
    return relative


def _source_to_rel(path: str) -> Path:
    relative = Path(path)
    if relative.is_absolute() or ".." in relative.parts:
        raise BuildError(f"Unsafe script source path cannot leave source root: source={path!r}.")
    if not relative.parts:
        raise BuildError(f"Expected non-empty script source path, got {path!r}.")
    return relative
