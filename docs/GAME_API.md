# Game API and Workflow

`pygodot` is a library-first framework. A game project imports `pygodot`, owns a
`Game` object, and calls methods on it.

## Basic workflow

```python
from pathlib import Path
from pygodot import Game

game = Game(
    name="MyGame",
    source_root=Path(__file__).parent,
    build_dir=Path(__file__).parent / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
)
```

Register scenes:

```python
game.add_scene(main_scene)
game.add_scene(menu_scene)
```

Register keyboard input actions:

```python
game.add_input_action("move_up", keys=["W", "UP"])
game.add_input_action("restart", keys=["SPACE"])
```

Set the generated project window size:

```python
game.set_window(size=Vec2(800, 600))
```

Generated scripts can use inline bodies, source files under `source_root`, or
simple template files:

```python
Script.from_file(
    source="scripts/main.gd",
    path="res://scripts/main.gd",
    extends="Node2D",
)

Script.from_template(
    source="scripts/player.gd.tmpl",
    path="res://scripts/player.gd",
    extends="Node2D",
    context={"speed": 300},
)
```

`Script.from_template(...)` uses Python's standard-library `string.Template`.
Supported placeholders are `$name`, `${name}`, and `$$` for a literal dollar
sign. This is plain text substitution for GDScript bodies, not Python-to-GDScript
transpilation.

Build or run:

```python
game.build()
game.run()
game.check_run(frames=20)
```

`check_run(...)` builds the project, imports it with Godot, runs a headless smoke
check for a fixed number of frames, captures logs, and raises on Godot script
errors.

## Current public API

```python
class Game:
    def add_scene(self, scene: Scene) -> None: ...
    def add_input_action(self, name: str, *, keys: list[str]) -> None: ...
    def set_window(self, *, size: Vec2) -> None: ...
    def build(self) -> BuildResult: ...
    def run(self, scene: str | None = None) -> None: ...
    def check_run(self, *, scene: str | None = None, frames: int = 20) -> GodotRunResult: ...
```

CLI commands, editor opening, import-only helpers, and export helpers are not
public API yet. If added later, they should delegate to `Game` instead of
becoming the primary workflow.

## Build result

`build()` returns structured information:

```python
@dataclass(frozen=True)
class BuildResult:
    project_dir: Path
    written_files: list[Path]
    generated_scenes: list[Path]
    generated_scripts: list[Path]
    copied_resources: list[Path]
    manifest_path: Path | None
```

## Entry point pattern

Game projects can use a normal Python file:

```python
game = Game(...)
game.add_scene(...)

if __name__ == "__main__":
    game.run()
```

This supports direct Python execution, IDE run/debug, tests that import the
`Game` object, and future thin CLI wrappers.
