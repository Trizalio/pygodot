# Architecture

`pygodot` is a layered generator for Godot 4 projects.

## Goal

Allow developers to describe Godot scenes and project structure using ordinary Python, then compile that description into native Godot files.

The generated output should be a normal Godot project that can be opened in the Godot editor, run, debugged, and exported.

## High-level pipeline

```text
User Python project
    ↓
Public DSL objects
    ↓
Normalization
    ↓
Typed IR
    ↓
Validation
    ↓
Emitters
    ↓
Generated Godot project
    ↓
Godot CLI import/run/export
```

## Layer 1 — User project

The user imports `pygodot` and defines a game with scenes, nodes, scripts, resources, and build/run commands.

Example direction:

```python
from pygodot import Game, Scene, Node2D, Label

game = Game(name="Example")
game.add_scene(Scene(path="res://scenes/main.tscn", root=Node2D("Main")))

game.build()
```

The user project is ordinary Python. It can use functions, loops, modules, constants, package managers, linters, formatters, and type checkers.

## Layer 2 — Public DSL

Public DSL objects represent user intent, not final `.tscn` syntax.

Examples:
- `Game`
- `Scene`
- `Node2D`
- `Control`
- `Label`
- `Button`
- `Script`
- `signal(...)`
- `Vec2`, `Vec3`, `Rect2`, `Color`, `NodePath`

The DSL should be explicit and boring. Avoid magic.

## Layer 3 — Normalized IR

The normalized IR is the internal compiler model.

Responsibilities:
- resolve paths;
- normalize property names and values;
- compute parent paths;
- collect external resources;
- create stable IDs;
- validate tree structure;
- detect duplicate sibling names;
- prepare emitter-friendly objects.

The IR should be separate from the public DSL because:
- public ergonomics and emitter needs differ;
- validation should not mutate user objects;
- tests can target the normalization boundary.

## Layer 4 — Validation

Validation should catch errors before writing files.

MVP validation:
- scene paths start with `res://`;
- node names are non-empty;
- node names do not contain `/`;
- sibling node names are unique;
- script paths start with `res://`;
- signal targets and methods are syntactically valid;
- supported value types are serializable by the emitter.

Future validation:
- property existence by Godot class;
- signal existence by Godot class;
- type checks against Godot API dump;
- resource type checks;
- path existence checks for assets.

## Layer 5 — Emitters

Emitters convert normalized IR into files.

MVP emitters:
- `ProjectEmitter` → `project.godot`
- `TscnEmitter` → `.tscn`
- `GdScriptEmitter` → `.gd`

Future emitters:
- `TresEmitter`
- `ExportPresetsEmitter`
- `ImportSettingsEmitter`
- `GodotAssistedEmitter`

Emitters should be deterministic and side-effect-light. File writing should be centralized in a build orchestrator.

## Layer 6 — Godot CLI integration

Godot CLI integration is optional for plain build, but useful for validation/run/export.

Expected operations:
- import resources in headless mode;
- run generated project;
- open editor;
- export debug/release builds;
- maybe dump Godot API for typed wrapper generation.

This layer should not be required to unit-test emitters.

## Suggested package layout

```text
src/pygodot/
  __init__.py
  game.py
  errors.py
  paths.py
  dsl/
    __init__.py
    scene.py
    nodes.py
    script.py
    signal.py
    values.py
    resources.py
  ir/
    __init__.py
    model.py
    normalize.py
    validate.py
  emitters/
    __init__.py
    project.py
    tscn.py
    gdscript.py
  build/
    __init__.py
    writer.py
    manifest.py
  godot_cli.py
```

## Build output direction

Recommended generated project structure:

```text
build/godot/
  .pygodot/
    manifest.json
  project.godot
  scenes/
    main.tscn
  scripts/
    main.gd
  assets/
    ...
```

If generated/manual separation is needed inside a long-lived Godot project:

```text
res://.generated/scenes/
res://.generated/scripts/
res://manual/scripts/
res://assets/
```

## Build manifest

`Game.build()` writes `res://.pygodot/manifest.json` in the generated Godot
project. The manifest records generated files, generated scenes/scripts, and
external resources.

For MVP build-directory output, external resources that already exist under
`Game.source_root` are copied to the same `res://` relative path inside the build
directory. Missing external resources remain referenced and are recorded with
`copied=false`.
