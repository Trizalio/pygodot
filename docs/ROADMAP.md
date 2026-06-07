# Roadmap

## MVP v0.1 — Direct scene generation

Goal: generate and run a minimal native Godot 4 project from a Python `Game` object.

Required features:
- package skeleton;
- `Game` library-first API;
- `Scene` model;
- basic nodes: `Node`, `Node2D`, `Control`, `Label`, `Button`;
- `Script` with raw GDScript body;
- signal connection model;
- simple value serialization;
- direct `.tscn` emitter;
- `project.godot` emitter;
- `.gd` emitter;
- build directory writer;
- generated/manual overwrite policy;
- `game.build()`;
- `game.run()` invoking Godot CLI;
- snapshot tests.

Definition of done:
- a Python game file can define one scene;
- build produces `project.godot`, `.tscn`, and `.gd`;
- generated project opens/runs in Godot 4;
- repeated builds produce stable diffs;
- tests verify emitted files.

## v0.2 — Better values and resources

Goal: remove MVP serialization hacks.

Features:
- `Vec2`, `Vec3`, `Color`, `NodePath`, `Rect2`, etc.;
- external resource references;
- texture references;
- generated resource IDs;
- asset copy/import manifest;
- manual script references;
- better validation errors.

## v0.3 — Typed wrappers and validation

Goal: improve correctness and IDE experience.

Features:
- typed node wrappers for common Godot classes;
- optional API dump ingestion;
- validation of property names/types where practical;
- signal validation where practical;
- richer error context with scene/node path.

## v0.4 — Project configuration

Goal: generate more of the Godot project.

Features:
- input map;
- autoloads;
- display/window settings;
- rendering settings;
- export presets;
- debug/release export commands;
- editor open command.

## v0.5 — Templates and manual boundaries

Goal: make generated GDScript useful without building a transpiler.

Features:
- `Script.from_file`;
- `Script.template`;
- generated file manifest;
- refusal to overwrite non-generated files;
- generated file cleanup for removed scenes/scripts.

## v0.6 — Godot-assisted emitter

Goal: support complex Godot resources safely.

Features:
- optional Godot headless generation scripts;
- `ResourceSaver`-based output for complex resources;
- support for resources that are brittle to write by hand;
- compare Godot-saved output in tests where possible.

## v1.0 — Usable framework foundation

Goal: a small but coherent framework suitable for real hobby projects.

Expected properties:
- library-first workflow;
- deterministic generation;
- good errors;
- normal Godot project output;
- clear generated/manual boundaries;
- useful DSL for common 2D/UI scenes;
- no Python runtime dependency in exported game.
