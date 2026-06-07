# Initial Codex Task Plan

This document lists a safe implementation sequence. Follow this order unless the user gives a different task.

## Task 1 — Package skeleton

Create a Python package layout under `src/pygodot/`.

Expected files:

```text
src/pygodot/__init__.py
src/pygodot/game.py
src/pygodot/errors.py
src/pygodot/dsl/__init__.py
src/pygodot/dsl/scene.py
src/pygodot/dsl/nodes.py
src/pygodot/dsl/script.py
src/pygodot/dsl/signal.py
src/pygodot/dsl/values.py
src/pygodot/ir/__init__.py
src/pygodot/ir/model.py
src/pygodot/ir/normalize.py
src/pygodot/ir/validate.py
src/pygodot/emitters/__init__.py
src/pygodot/emitters/project.py
src/pygodot/emitters/tscn.py
src/pygodot/emitters/gdscript.py
src/pygodot/build/__init__.py
src/pygodot/build/writer.py
src/pygodot/godot_cli.py
```

## Task 2 — Public DSL dataclasses

Implement minimal public DSL:
- `Game`
- `Scene`
- `Node`
- node wrappers: `Node2D`, `Control`, `Label`, `Button`
- `Script`
- `SignalConnection`
- `signal(...)`
- basic values: `Vec2`, `Vec3`, `Color`, `NodePath`

## Task 3 — Normalized IR

Create IR dataclasses separate from DSL.

IR should include:
- scene path;
- normalized root node;
- node paths;
- normalized properties;
- external resources;
- signal connections;
- stable resource IDs.

## Task 4 — Validation

Implement validation before emission:
- valid paths;
- valid names;
- duplicate sibling names;
- supported values;
- scripts have valid paths;
- signal fields are non-empty.

## Task 5 — Emitters

Implement string emitters:
- `ProjectEmitter.emit(project_ir) -> str`
- `TscnEmitter.emit(scene_ir) -> str`
- `GdScriptEmitter.emit(script_ir) -> str`

Do not write files directly from emitters unless the design explicitly chooses that.

## Task 6 — Build writer

Implement file writing with generated/manual overwrite policy.

At minimum:
- create build directory;
- write generated files;
- include final newline;
- refuse unsafe overwrite in persistent dirs.

## Task 7 — `Game.build()`

Wire the pipeline:

```text
Game scenes → normalize → validate → emit → write files
```

Return `BuildResult`.

## Task 8 — `Game.run()`

Implement Godot CLI helper:

```python
game.run()
```

It should call build if needed or assume build exists based on explicit design.

Do not make Godot required for unit tests.

## Task 9 — Tests

Add tests for:
- value serialization;
- minimal `.tscn` snapshot;
- script emission;
- project emission;
- duplicate node names;
- stable output across repeated builds.

## Task 10 — Example project

Add a minimal example under `examples/minimal/` showing:
- `Game` object;
- one scene;
- a label;
- a button;
- raw GDScript signal handler;
- `game.build()` and `game.run()` in `if __name__ == "__main__"`.

## Do not do yet

Do not implement:
- Python runtime in Godot;
- Python-to-GDScript transpiler;
- complex resource generation;
- metaclass DSL;
- context-manager scene construction DSL;
- mandatory JSON/YAML IR;
- broad Godot API wrapper generation.
