# Codex Instructions for `pygodot`

This repository is intended to become a Python 3 framework for declaring Godot 4 games/scenes in Python and compiling them into a native Godot project.

Follow these instructions when making changes in this repository.

## Core product direction

`pygodot` is a **build-time Python library**, not a Python runtime for Godot.

The user writes ordinary Python code using `pygodot` as a library. That Python code constructs an in-memory game/scene model. The framework then emits a native Godot 4 project: `.tscn`, `.gd`, `.tres`, `project.godot`, resource files, and optional generated support code.

The generated Godot project must remain normal, openable, debuggable, and runnable by Godot 4.

## Non-negotiable decisions

1. **No JSON/YAML intermediate representation as the main architecture.**
   - Python DSL objects should normalize into typed Python IR objects.
   - JSON/YAML dumps may exist later for debugging, cache inspection, or snapshots, but not as the main compilation boundary.

2. **Start with a fast direct `.tscn` emitter.**
   - MVP should generate simple Godot 4 text scenes directly.
   - Do not introduce a mandatory Godot-assisted generation step for simple scenes.
   - A Godot-assisted emitter may be added later for complex resources.

3. **Python is design/build-time only. Runtime logic is GDScript.**
   - Do not implement Python-in-Godot runtime.
   - Do not depend on godot-python/GDExtension Python bindings.
   - Do not build a Python subset transpiler in MVP.
   - Raw/template GDScript generation is acceptable.

4. **Avoid metaclasses and context-manager DSL magic in the public API.**
   - Prefer explicit, typed, importable Python objects and functions.
   - IDE autocomplete, type checking, linting, and ordinary Python composition are more important than clever syntax.

5. **`pygodot` must be a library first, CLI second.**
   - Do not design the primary workflow as `python compile.py game.py`.
   - The game project should import `pygodot` and create a `Game` object.
   - Compilation and run should be methods of that object, e.g. `game.build()`, `game.run()`, `game.export()`.
   - A CLI wrapper may exist later, but it should delegate to project/library entrypoints.

6. **Generated code must have explicit ownership boundaries.**
   - Never silently overwrite user-owned/manual files.
   - Generated files should live under explicit generated paths or be clearly marked.

## Preferred high-level architecture

```text
Python user project
  imports pygodot
  declares Game / Scenes / Nodes / Scripts
        ↓
Public DSL objects
        ↓
Typed normalized IR
        ↓
Validation and path/resource resolution
        ↓
Emitters
  - project.godot
  - .tscn
  - .gd
  - .tres later
        ↓
Optional Godot CLI validation/import/run/export
```

## Repository implementation expectations

When adding code, keep modules small and layered:

```text
src/pygodot/
  __init__.py
  game.py              # Game object and public orchestration API
  dsl/
    nodes.py           # Public node constructors/classes
    scene.py
    script.py
    resources.py
    values.py          # Vec2, Vec3, Color, NodePath, ExtResource, etc.
  ir/
    model.py           # Normalized IR dataclasses
    normalize.py       # DSL -> IR
    validate.py
  emitters/
    tscn.py
    gdscript.py
    project.py
  godot_cli.py         # Godot binary invocation helpers
  errors.py
```

Do not create a monolithic compiler script except as a throwaway prototype.

## Public API shape

The intended user workflow should look approximately like this:

```python
from pathlib import Path
from pygodot import Game, Scene, Node2D, Label, Button, Script, signal

main_script = Script(
    path="res://scripts/main.gd",
    extends="Node2D",
    body="""
var counter := 0

func _ready() -> void:
    $Title.text = "Generated from Python DSL"

func _on_start_pressed() -> void:
    counter += 1
    $Title.text = "Clicked %s times" % counter
""",
)

game = Game(
    name="GeneratedGame",
    source_root=Path(__file__).parent,
    build_dir=Path(__file__).parent / "build" / "godot",
    main_scene="res://scenes/main.tscn",
)

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Node2D(
            "Main",
            script=main_script,
            children=[
                Label("Title", text="Generated scene", position=(80, 60)),
                Button(
                    "StartButton",
                    text="Click me",
                    position=(80, 120),
                    signals=[signal("pressed", target=".", method="_on_start_pressed")],
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.build()
    game.run()
```

This is illustrative, not a frozen final API. Preserve the direction: library-first, explicit objects, no magic.

## Runtime strategy

MVP runtime must be ordinary Godot 4 with GDScript.

Allowed:
- emitting `.gd` files from raw string bodies;
- emitting `.gd` files from simple templates later;
- attaching generated or user-provided GDScript scripts to nodes;
- invoking Godot CLI for import/run/export.

Not allowed in MVP:
- embedding CPython in Godot;
- godot-python runtime;
- Python subset transpilation to GDScript;
- complex AST-to-GDScript compiler;
- runtime scene construction as the primary generated output.

## `.tscn` emitter constraints

MVP emitter should support:
- root node;
- child nodes;
- simple properties;
- `Vector2`/`Vector3`/`Color`/`NodePath` values;
- external script resources;
- signal connections;
- deterministic output ordering;
- stable resource IDs.

Do not optimize prematurely for every Godot resource type. Add explicit support incrementally.

## Testing expectations

Use snapshot tests for emitted `.tscn`, `.gd`, and `project.godot` outputs.

Important properties:
- deterministic output across runs;
- stable resource IDs;
- no duplicate sibling node names;
- correct parent paths;
- valid signal connection paths;
- no accidental mutation of source DSL objects during emission.

## Style expectations

- Python 3.11+ syntax is allowed.
- Prefer dataclasses or attrs/Pydantic only where they help. Do not add Pydantic as a dependency unless validation requirements justify it.
- Use `dict`, `list`, `T | None`, and modern type syntax.
- Keep public errors explicit and useful.
- Keep generated files deterministic and readable.
- Avoid hidden global registries unless they are clearly isolated.

## Documentation expectations

When decisions change, update the relevant Markdown files in `docs/`.

Start with these documents:
- `docs/DECISIONS.md`
- `docs/ARCHITECTURE.md`
- `docs/DSL.md`
- `docs/GAME_API.md`
- `docs/EMITTERS.md`
- `docs/RUNTIME.md`
- `docs/ROADMAP.md`
- `docs/TESTING.md`
- `docs/OPEN_QUESTIONS.md`
