# Game API and Workflow

`pygodot` should be a library-first framework. The user should import it from the game project and control build/run through a `Game` object.

## Rejected primary workflow

Avoid making this the primary workflow:

```bash
python compile.py game.py
```

Problems:
- weak IDE integration;
- awkward import model;
- difficult composition with other libraries/build systems;
- encourages monolithic compiler-script design;
- makes the game definition feel like data passed to a tool instead of a Python project.

## Preferred workflow

The game project owns a `Game` object:

```python
from pathlib import Path
from pygodot import Game

game = Game(
    name="MyGame",
    source_root=Path(__file__).parent,
    build_dir=Path(__file__).parent / "build" / "godot",
    main_scene="res://scenes/main.tscn",
)
```

Then the project registers scenes/resources:

```python
game.add_scene(main_scene)
game.add_scene(menu_scene)
```

Then it calls:

```python
game.build()
game.import_resources()
game.run()
game.open_editor()
game.export(preset="Linux/X11", release=True)
```

## CLI role

A CLI is allowed but should be secondary:

```bash
pygodot run path.to.game:game
pygodot build path.to.game:game
```

The CLI should import a `Game` object and call its methods. It should not own the compiler architecture.

## Suggested `Game` responsibilities

`Game` should orchestrate:
- project metadata;
- scene registration;
- resource registration;
- build directory policy;
- generated/manual file policy;
- emitters;
- Godot CLI integration;
- build manifests.

`Game` should not contain all emitter logic directly.

## Possible API sketch

```python
class Game:
    def __init__(
        self,
        *,
        name: str,
        source_root: Path,
        build_dir: Path,
        main_scene: str,
        godot_bin: str = "godot",
    ) -> None: ...

    def add_scene(self, scene: Scene) -> None: ...
    def build(self) -> BuildResult: ...
    def import_resources(self) -> None: ...
    def run(self, scene: str | None = None) -> None: ...
    def open_editor(self) -> None: ...
    def export(self, *, preset: str, release: bool = True) -> None: ...
```

## Build result

`build()` should return structured information rather than only printing text:

```python
@dataclass(frozen=True)
class BuildResult:
    project_dir: Path
    written_files: list[Path]
    generated_scenes: list[Path]
    generated_scripts: list[Path]
```

## Entry point file pattern

A game project can use a normal Python file:

```python
# game.py

game = Game(...)
game.add_scene(...)

if __name__ == "__main__":
    game.build()
    game.run()
```

This supports:
- direct Python execution;
- IDE run/debug;
- import by tests;
- import by CLI;
- custom build scripts.
