"""Library-first game orchestration API."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from pygodot.build.writer import GeneratedFileWriter
from pygodot.dsl.scene import Scene
from pygodot.errors import BuildError
from pygodot.emitters.gdscript import GdScriptEmitter
from pygodot.emitters.project import ProjectEmitter
from pygodot.emitters.tscn import TscnEmitter
from pygodot.godot_cli import import_project, run_project
from pygodot.ir.model import IRNode, IRScript
from pygodot.ir.normalize import normalize_project
from pygodot.ir.validate import validate_project


@dataclass(slots=True, frozen=True)
class BuildResult:
    """Structured result returned by Game.build()."""

    project_dir: Path
    written_files: list[Path]
    generated_scenes: list[Path]
    generated_scripts: list[Path]


@dataclass(slots=True)
class Game:
    """A user-owned Godot project declaration."""

    name: str
    source_root: Path
    build_dir: Path
    main_scene: str
    godot_bin: str = "godot"
    scenes: list[Scene] = field(default_factory=list)

    def add_scene(self, scene: Scene) -> None:
        self.scenes.append(scene)

    def build(self) -> BuildResult:
        project = normalize_project(name=self.name, main_scene=self.main_scene, scenes=self.scenes)
        validate_project(project)

        writer = GeneratedFileWriter(self.build_dir, allow_overwrite_unmarked=True)
        project_emitter = ProjectEmitter()
        scene_emitter = TscnEmitter()
        script_emitter = GdScriptEmitter()

        written_files: list[Path] = []
        generated_scenes: list[Path] = []
        generated_scripts: list[Path] = []

        written_files.append(writer.write_text(Path("project.godot"), project_emitter.emit(project)))

        emitted_script_paths: set[str] = set()
        for scene in project.scenes:
            for script in _iter_scripts(scene.root):
                if not script.generated:
                    continue
                if script.path in emitted_script_paths:
                    continue
                emitted_script_paths.add(script.path)
                script_path = writer.write_text(_res_to_rel(script.path), script_emitter.emit(script))
                written_files.append(script_path)
                generated_scripts.append(script_path)

            scene_path = writer.write_text(_res_to_rel(scene.path), scene_emitter.emit(scene))
            written_files.append(scene_path)
            generated_scenes.append(scene_path)

        return BuildResult(
            project_dir=self.build_dir,
            written_files=written_files,
            generated_scenes=generated_scenes,
            generated_scripts=generated_scripts,
        )

    def run(self, scene: str | None = None) -> None:
        result = self.build()
        import_project(result.project_dir, godot_bin=self.godot_bin)
        run_project(result.project_dir, godot_bin=self.godot_bin, scene=scene or self.main_scene)


def _iter_scripts(node: IRNode) -> list[IRScript]:
    scripts: list[IRScript] = []
    if node.script is not None:
        scripts.append(node.script)
    for child in node.children:
        scripts.extend(_iter_scripts(child))
    return scripts


def _res_to_rel(path: str) -> Path:
    if not path.startswith("res://"):
        raise BuildError(f"Expected res:// path, got {path!r}.")
    return Path(path.removeprefix("res://"))
