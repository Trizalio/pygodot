# Roadmap

## MVP v0.1 - Direct scene generation

Status: implemented.

Goal: generate and run a minimal native Godot 4 project from a Python `Game` object.

Required features:
- done: package skeleton;
- done: `Game` library-first API;
- done: `Scene` model;
- done: basic nodes: `Node`, `Node2D`, `Control`, `Label`, `Button`;
- done: `Script` with raw GDScript body;
- done: signal connection model;
- done: simple value serialization;
- done: direct `.tscn` emitter;
- done: `project.godot` emitter;
- done: `.gd` emitter;
- done: build directory writer;
- done: generated/manual overwrite policy;
- done: `game.build()`;
- done: `game.run()` invoking Godot CLI;
- done: snapshot tests.

Definition of done:
- done: a Python game file can define one scene;
- done: build produces `project.godot`, `.tscn`, and `.gd`;
- done: generated project opens/runs in Godot 4;
- done: repeated builds produce stable diffs;
- done: tests verify emitted files.

Notes:
- the old `src/compiler.py` prototype has been removed;
- the library-first example lives in `examples/minimal/`;
- tests currently use `unittest` so they run without extra dependencies.

## v0.2 - Better values and resources

Status: mostly implemented.

Goal: remove MVP serialization hacks.

Features:
- done: `Vec2`, `Vec3`, `Color`, `NodePath`, `Rect2`;
- done: external resource references via `ext_resource(...)`;
- done: texture references via `texture(...)`;
- done: packed scene references via `packed_scene(...)`;
- done: generated resource IDs;
- done: asset copy/import manifest at `.pygodot/manifest.json`;
- done: manual script references via `Script.reference(...)`;
- done: better validation errors with scene/node/property/resource context.

Remaining before v0.3:
- decide whether v0.2 needs any more explicit value wrappers beyond `Rect2`;
- decide whether missing external resources should remain `copied=false` or become warnings/errors;
- optionally add a small example that demonstrates copied assets and manual script references.

## v0.3 - Typed wrappers and validation

Status: not started.

Goal: improve correctness and IDE experience.

Features:
- typed node wrappers for common Godot classes;
- optional API dump ingestion;
- validation of property names/types where practical;
- signal validation where practical;
- richer error context with scene/node path.

## v0.4 - Project configuration

Status: not started.

Goal: generate more of the Godot project.

Features:
- input map;
- autoloads;
- display/window settings;
- rendering settings;
- export presets;
- debug/release export commands;
- editor open command.

## v0.5 - Templates and manual boundaries

Status: not started.

Goal: make generated GDScript useful without building a transpiler.

Features:
- `Script.from_file`;
- `Script.template`;
- generated file manifest;
- refusal to overwrite non-generated files;
- generated file cleanup for removed scenes/scripts.

## v0.6 - Godot-assisted emitter

Status: not started.

Goal: support complex Godot resources safely.

Features:
- optional Godot headless generation scripts;
- `ResourceSaver`-based output for complex resources;
- support for resources that are brittle to write by hand;
- compare Godot-saved output in tests where possible.

## v1.0 - Usable framework foundation

Status: future target.

Goal: a small but coherent framework suitable for real hobby projects.

Expected properties:
- library-first workflow;
- deterministic generation;
- good errors;
- normal Godot project output;
- clear generated/manual boundaries;
- useful DSL for common 2D/UI scenes;
- no Python runtime dependency in exported game.
