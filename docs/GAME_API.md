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

Register autoload singletons:

```python
game.add_autoload("GameState", "res://scripts/singletons/game_state.gd")
game.add_autoload("SceneChanger", "res://scripts/singletons/scene_changer.gd")
```

Set project-level display and settings:

```python
game.set_icon("res://resources/icon.png")
game.set_display(size=Vec2(540, 750), stretch_mode="canvas_items", stretch_aspect="expand")
game.set_project_setting("audio/output_latency/web", 200)
game.set_project_setting("physics/common/enable_pause_aware_picking", True)
```

Register input actions:

```python
game.add_input_action("move_up", keys=["W", "UP"])
game.add_input_action("restart", keys=["SPACE"])
game.add_input_action("shoot", mouse_buttons=["LEFT"])
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
    def add_autoload(self, name: str, path: str) -> None: ...
    def set_icon(self, path: str) -> None: ...
    def set_display(
        self,
        *,
        size: Vec2,
        stretch_mode: str | None = None,
        stretch_aspect: str | None = None,
    ) -> None: ...
    def set_project_setting(self, path: str, value: Any) -> None: ...
    def add_input_action(
        self,
        name: str,
        *,
        keys: list[str] | None = None,
        mouse_buttons: list[str] | None = None,
    ) -> None: ...
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
    generated_resources: list[Path]
    copied_resources: list[Path]
    referenced_resources: list[str]
    manifest_path: Path | None
```

`referenced_resources` contains `res://` paths that pygodot intentionally did
not write or copy, such as manual scripts and missing or externally managed
assets. The manifest records the same resources with `ownership="referenced"`.

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
