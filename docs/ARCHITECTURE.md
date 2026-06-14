# Architecture

`pygodot` is a layered generator for native Godot 4 projects.

## Goal

Developers describe scenes and project structure with ordinary Python. `pygodot`
normalizes that description into typed IR, validates it, and emits normal Godot
files.

The generated project should be openable, debuggable, and runnable by Godot 4.

## Pipeline

```text
User Python project
  -> Public DSL objects
  -> Normalized IR
  -> Validation
  -> Emitters
  -> Generated Godot project
  -> Optional Godot CLI import/run/check
```

## User project

The user project is ordinary Python. It can use modules, functions, constants,
loops, package managers, linters, and type checkers.

The source Python project owns the `Game` object and remains the source of
truth. Generated Godot files are build output.

## Public DSL

Public DSL objects represent user intent, not final `.tscn` syntax.

Current public concepts include:

- `Game`;
- `Scene`;
- `Node` and `node(...)`;
- node constructors: `Node2D`, `Control`, `ColorRect`, `Sprite2D`,
  `Label`, `Button`, `Timer`, `AnimationPlayer`, `AudioStreamPlayer`,
  `Area2D`, `CollisionShape2D`;
- `Script` and `Script.reference(...)`;
- `signal(...)`;
- `InputAction` through `Game.add_input_action(...)`;
- values: `Vec2`, `Vec3`, `Rect2`, `Color`, `NodePath`;
- external resources: `ext_resource(...)`, `texture(...)`,
  `audio_stream(...)`, `font(...)`, `packed_scene(...)`;
- scene instances: `scene_instance(...)`.
- animations: `animation(...)`, `value_track(...)`, `key(...)`.
- shape resources: `rectangle_shape_2d(...)`.

The DSL should stay explicit and boring. Avoid hidden global scene stacks,
metaclass-heavy APIs, and mandatory context managers.

## Normalized IR

The normalized IR is the internal compiler model.

Responsibilities:

- compute node and parent paths;
- normalize property values;
- normalize scene instance resources;
- normalize animation sub-resources;
- normalize generated shape sub-resources;
- collect external resources;
- compute stable resource IDs;
- carry project-level input actions;
- carry project-level window settings;
- prepare emitter-friendly objects.

Validation should not mutate public DSL objects.

## Validation

Validation catches errors before writing files.

Current validation includes:

- `res://` scene, script, and resource paths;
- non-empty node names and types;
- no `/` in node names;
- duplicate sibling node detection;
- generated/manual script ownership checks;
- serializable property values;
- non-empty signal names, targets, and methods;
- registered `main_scene`;
- keyboard input action names, duplicates, and supported keys.

Future validation may use Godot API data to check property names, property
types, signal names, and resource types.

## Emitters

Emitters convert normalized IR into strings.

Current emitters:

- `ProjectEmitter` -> `project.godot`;
- `TscnEmitter` -> `.tscn`;
- `GdScriptEmitter` -> `.gd`.

Emitters should be deterministic and side-effect-light. File writing belongs to
the build layer.

## Build layer

`Game.build()` writes a generated Godot project under `build_dir`.
It also copies existing source-owned external resources from `source_root` to
matching `res://` paths under `build_dir`.

Current build output:

```text
build/godot_project/
  .pygodot/
    manifest.json
  project.godot
  scenes/
  scripts/
  assets/
```

The generated/manual ownership rules are documented in
`docs/GENERATED_BOUNDARY.md`.

## Godot CLI integration

Godot is not required for emitter/unit tests.

Current Godot CLI helpers:

- import generated resources before run/check;
- run the generated project;
- run a headless smoke check with captured logs.

Future work may add editor opening and export helpers.
