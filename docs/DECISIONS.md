# Architecture Decisions

This document records current project decisions. Historical decision churn
belongs in git.

## D001 - Python Is Build-Time Only

Status: accepted.

Python describes and generates a Godot 4 project. Python code does not run
inside the exported game.

Runtime logic is ordinary GDScript attached to generated or user-owned Godot
scenes.

Consequences:

- gameplay logic is written in GDScript;
- Python can generate `.gd` files;
- Python-in-Godot runtimes and Python-to-GDScript transpilation are out of
  scope.

## D002 - No JSON/YAML Main IR

Status: accepted.

The compiler pipeline is:

```text
Python DSL objects -> typed Python IR -> emitters
```

JSON/YAML may be used later for debugging or cache inspection, but not as the
primary compilation boundary.

## D003 - Direct `.tscn` Emitter First

Status: accepted.

Simple Godot 4 text scenes are emitted directly.

Reasons:

- fast builds;
- deterministic output;
- readable generated files;
- snapshot-testable emission;
- no Godot dependency for normal builds.

Godot-assisted emission is reserved for complex resources where direct text
generation becomes brittle.

## D004 - Explicit DSL

Status: accepted.

The public DSL uses explicit Python objects and functions.

Avoid:

- mandatory context managers;
- metaclass-heavy scene syntax;
- hidden global scene stacks;
- import-time magic.

## D005 - Library-First API

Status: accepted.

The game project owns a `Game` object:

```python
game = Game(...)
game.add_scene(...)
game.build()
game.run()
```

A CLI may exist later, but it should import a `Game` object and call its methods.

## D006 - Generated/Manual Boundary

Status: accepted.

Generated files are build output. The Python source project, manual assets, and
explicitly referenced manual scripts are the source of truth.

The current policy is documented in `docs/GENERATED_BOUNDARY.md`.

## D007 - Stable Output Is A Feature

Status: accepted.

Generated output must be deterministic across runs with the same input.

Implementation implications:

- stable resource IDs;
- stable node order;
- stable property order;
- stable manifest order;
- no timestamps in generated files.
