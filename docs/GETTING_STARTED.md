# Getting Started

This tutorial starts from an empty folder outside the `pygodot` repository. It
uses `pygodot` as an installed Python package and builds a normal Godot 4
project.

Godot is optional for the build-only path. You only need Godot when running the
generated project or the smoke check.

## 1. Install pygodot From A Checkout

From any terminal:

```powershell
python -m pip install -e C:\path\to\pygodot
```

Use the path to your local `pygodot` checkout.

## 2. Create A Project Folder

```powershell
mkdir my_game
cd my_game
```

## 3. Write `game.py`

Create `game.py`:

```python
from pathlib import Path

from pygodot import Button, Game, Label, Node2D, Scene, Script, Vec2, signal


ROOT = Path(__file__).parent

main_script = Script(
    path="res://scripts/main.gd",
    extends="Node2D",
    body="""
var counter := 0

func _ready() -> void:
    $Title.text = "Built with pygodot"

func _on_start_pressed() -> void:
    counter += 1
    $Title.text = "Clicked %s times" % counter
""",
)

game = Game(
    name="MyPygodotGame",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot",
    main_scene="res://scenes/main.tscn",
)

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Node2D(
            "Main",
            script=main_script,
            children=[
                Label("Title", text="Ready", position=Vec2(80, 60)),
                Button(
                    "StartButton",
                    text="Click me",
                    position=Vec2(80, 120),
                    signals=[signal("pressed", target=".", method="_on_start_pressed")],
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.build()
```

## 4. Build The Godot Project

```powershell
python game.py
```

This writes a generated Godot project under:

```text
build/godot/
```

Inspect the generated files:

```text
build/godot/project.godot
build/godot/scenes/main.tscn
build/godot/scripts/main.gd
build/godot/.pygodot/manifest.json
```

Generated files are build output. Edit `game.py` and your source files, then
run `python game.py` again.

## 5. Run With Godot

If your Godot executable is not available as `godot`, set `GODOT_BIN`:

```powershell
$env:GODOT_BIN = "C:\Path\To\Godot.exe"
```

Then change the final line of `game.py` while you are actively trying the game:

```python
if __name__ == "__main__":
    game.run()
```

## 6. Move The Script To A File

Create a source-owned script file:

```powershell
mkdir scripts
```

Create `scripts/main.gd`:

```gdscript
var counter := 0

func _ready() -> void:
    $Title.text = "Script loaded from file"

func _on_start_pressed() -> void:
    counter += 1
    $Title.text = "Clicked %s times" % counter
```

Save GDScript files as UTF-8 without BOM. Godot may report a parse error if a
BOM character is present in a `.gd` file.

Replace the `main_script = Script(...)` block in `game.py` with:

```python
main_script = Script.from_file(
    source="scripts/main.gd",
    path="res://scripts/main.gd",
    extends="Node2D",
)
```

Build again:

```powershell
python game.py
```

`scripts/main.gd` is user-owned source input. `build/godot/scripts/main.gd` is
generated output with the `extends Node2D` header added by `pygodot`.

## 7. Add A Generated `.tres` Resource

Import `Color` and `label_settings`:

```python
from pygodot import Button, Color, Game, Label, Node2D, Scene, Script, Vec2, label_settings, signal
```

Add this near `main_script`:

```python
title_settings = label_settings(
    "res://ui/title_label_settings.tres",
    font_size=28,
    font_color=Color(0.9, 0.95, 1.0),
)
```

Pass it to the title label:

```python
Label(
    "Title",
    text="Ready",
    position=Vec2(80, 60),
    label_settings=title_settings,
)
```

Build again. The generated project now includes:

```text
build/godot/ui/title_label_settings.tres
```

The manifest records the `.tres` resource as generated.

## 8. Optional Smoke Check

When Godot is available, run a short headless check:

```powershell
python -c "from game import game; result = game.check_run(frames=20); print(result.returncode)"
```

If the smoke check fails, `pygodot` prints a diagnostic summary with the command,
return code, stdout tail, stderr tail, and Godot log tail.
