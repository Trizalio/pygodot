# Architecture Decisions

This document records the current project decisions. Treat it as the source of truth unless superseded by a later explicit decision.

## D001 — Python is build-time only

Status: accepted.

`pygodot` uses Python to describe and generate a Godot 4 project. Python code does not run inside the exported game in MVP.

Runtime logic is ordinary GDScript attached to generated or user-owned Godot scenes.

Rationale:
- avoids unstable Python/Godot runtime bindings;
- keeps generated projects native to Godot;
- avoids export/distribution problems;
- avoids CPython/GIL/platform packaging concerns;
- matches the actual goal: remove editor boilerplate, not replace Godot runtime.

Consequences:
- gameplay logic is written in GDScript for MVP;
- Python can generate boilerplate `.gd` files;
- Python subset transpilation is out of scope for MVP.

## D002 — No JSON/YAML main IR

Status: accepted.

The main compilation pipeline is:

```text
Python DSL objects → typed Python IR → emitters
```

JSON/YAML may later be used for debug dumps, cache inspection, or snapshot testing, but not as the primary compiler boundary.

Rationale:
- Python is already the source language;
- typed Python objects are easier to validate and refactor;
- JSON/YAML would add serialization noise without solving the core problem;
- object references, resources, and paths are easier to handle in Python IR.

## D003 — Start with direct `.tscn` emitter

Status: accepted.

MVP directly emits simple Godot 4 `.tscn` text scenes.

Rationale:
- fast;
- deterministic;
- easy to snapshot-test;
- does not require Godot for the compile step;
- produces reviewable files.

Future extension:
- add a Godot-assisted emitter for complex resources such as Animation, TileSet, Theme, Mesh, ShaderMaterial, or imported assets when direct text generation becomes too brittle.

## D004 — Avoid metaclass/context-manager DSL magic

Status: accepted.

The public DSL should be explicit Python object construction, functions, and ordinary composition.

Rationale:
- IDE autocomplete matters;
- static analysis and linting matter;
- the framework should be understandable to Python developers;
- hidden global state makes scene generation difficult to debug.

## D005 — Library-first API

Status: accepted.

`pygodot` must be primarily a library imported by the game project. The game code should own a `Game` object and call methods on it.

Preferred workflow:

```python
game = Game(...)
game.add_scene(...)
game.build()
game.run()
```

A CLI may exist, but it should be a thin wrapper around project/library entrypoints.

Rationale:
- better IDE support;
- easier integration with arbitrary build systems;
- no special `compile.py game.py` protocol;
- makes the project feel like a Python package, not a one-off script runner.

## D006 — Generated/manual file boundaries

Status: accepted.

Generated files must be clearly separated from user-owned files.

Possible policies:
- generated files live under `res://.generated/`;
- generated files include a clear header comment;
- compiler refuses to overwrite files without a generated marker;
- manual scripts/resources live under explicit manual paths.

MVP should choose one clear policy and enforce it.

## D007 — Stable output is a feature

Status: accepted.

Generated output must be deterministic across runs with the same input.

Rationale:
- clean Git diffs;
- reliable snapshot tests;
- easier debugging;
- fewer false changes in generated Godot project files.

Implementation implications:
- stable resource IDs;
- stable node order;
- stable property order;
- stable path normalization.
