# pygodot: Next Codex Roadmap

This is the working roadmap for upcoming `pygodot` development. It should stay
short, current, and focused on work that has not been completed yet. Completed
sprint history belongs in git commits, not in this file.

Follow the priorities in order unless the user explicitly changes direction.

## Current Baseline

`pygodot` is a build-time Python library for declaring Godot 4 projects and
generating ordinary Godot files.

Implemented:

- library-first `Game` API with `build()`, `run()`, and `check_run()`;
- explicit scene/node/script DSL;
- selected node constructors plus generic `node(...)`;
- typed values: `Vec2`, `Vec3`, `Rect2`, `Color`, `NodePath`;
- external resource helpers for textures, audio, fonts, packed scenes, and
  generic resources;
- generated scenes, scripts, `.tres` resources, and `project.godot`;
- generated `LabelSettings` and narrow `StyleBoxFlat` resources;
- generated sub-resources for simple shapes and animations;
- scene instancing through generated or manual `PackedScene` resources;
- keyboard-only InputMap generation;
- minimal window settings;
- explicit generated/copied/referenced resource ownership in the build
  manifest;
- optional real Godot smoke checks;
- minimal GitHub Actions unit-test CI that does not require Godot.

The README is the user-facing navigation page. Detailed API and behavior notes
live in focused docs such as `docs/DSL.md`, `docs/EMITTERS.md`,
`docs/GENERATED_BOUNDARY.md`, and `docs/TESTING.md`.

## Development Rules

- Keep changes small and milestone-focused.
- Do not add unrelated features while implementing a milestone.
- Preserve examples unless the milestone explicitly changes one.
- Preserve snapshots unless generated output intentionally changes.
- Keep public API additions example-backed, documented, exported, and tested.
- Use `node(...)` for uncommon Godot nodes before adding convenience
  constructors.
- Keep ordinary unit tests independent of Godot.
- Use `tools/smoke_examples.py` only for optional real Godot verification.

## Candidate Next Milestones

### 1. Resource Dependency Boundaries

Goal: make copied/manual resource dependency behavior explicit before adding
broader asset features.

Possible tasks:

- document what pygodot does and does not discover inside copied `.tres` files;
- add tests for referenced-but-missing external assets with
  `ownership="referenced"`;
- decide whether missing copied assets should remain soft references or become
  opt-in validation errors;
- keep scope away from a full asset graph engine.

Anti-goals:

- no import pipeline;
- no cleanup/pruning;
- no broad resource graph engine.

### 2. Godot Error Reporting Polish

Goal: make `Game.check_run()` and smoke failures easier to diagnose.

Possible tasks:

- improve returned log snippets or error summaries;
- add tests for command/log handling without requiring Godot;
- keep the Godot execution path optional.

Anti-goals:

- no CI dependency on Godot;
- no editor integration.

### 3. InputMap Increment

Goal: extend InputMap only when a concrete example needs it.

Possible tasks:

- add one small example-backed input capability, such as mouse button or gamepad
  button support;
- keep keyboard behavior unchanged;
- add project emitter tests and example assertions.

Anti-goals:

- no full input abstraction layer;
- no generated wrappers for every Godot input event.

## Standing Non-Goals

Do not implement these unless the user explicitly changes direction:

- Python runtime inside Godot;
- Python-to-GDScript transpiler;
- GDExtension Python integration;
- full Godot API wrapper generation;
- visual editor replacement;
- ECS;
- broad physics DSL;
- complete resource DSL for all Godot resources;
- export presets and release packaging;
- Godot-assisted emitter;
- complex UI layout framework;
- full `Theme` generation;
- CI that requires Godot.

## Definition Of Done

A milestone is complete only when:

- relevant unit tests pass;
- generated output remains deterministic;
- snapshots are updated only intentionally;
- docs are updated when public behavior changes;
- examples still build;
- optional real Godot smoke checks pass when the task touches examples and Godot
  is available;
- public API exports are updated if a new public helper is introduced.
