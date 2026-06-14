# pygodot: Next Development Roadmap for Codex

This document is the working roadmap for the next pygodot development iterations.

It is intended to be read by Codex before making changes. Follow the milestones in order unless the user explicitly asks otherwise.

## Current project baseline

`pygodot` is a build-time Python library for declaring Godot 4 projects and generating normal Godot project files.

Core principles that must remain unchanged:

- Python is used at build time only.
- Runtime logic remains ordinary GDScript.
- Do not introduce Python runtime inside Godot.
- Do not build a Python-to-GDScript transpiler.
- Do not introduce JSON/YAML as the main intermediate representation.
- Keep the internal pipeline as: Python DSL -> normalized IR -> emitters.
- Prefer direct `.tscn`, `.gd`, `.tres`/resource emitters where practical.
- Keep generated output deterministic and snapshot-testable.
- Prefer library-first usage through `Game`, not command-line-only workflows.

Current implemented surface includes:

- `Game.build()`, `Game.run()`, `Game.check_run()`.
- Public scene/node/script DSL.
- Generic `node(...)` helper.
- Selected node constructors:
  - `Node2D`
  - `Control`
  - `ColorRect`
  - `Sprite2D`
  - `Label`
  - `Button`
  - `Timer`
  - `AnimationPlayer`
  - `AudioStreamPlayer`
  - `Area2D`
  - `CollisionShape2D`
- Typed value wrappers:
  - `Vec2`
  - `Vec3`
  - `Rect2`
  - `Color`
  - `NodePath`
- External resources:
  - `ext_resource(...)`
  - `texture(...)`
  - `audio_stream(...)`
  - `font(...)`
  - `packed_scene(...)`
- Scene instances through `scene_instance(...)`.
- Generated value-track animations through `animation(...)`.
- Generic generated scene sub-resources through `sub_resource(...)`.
- Generated shape resources through `rectangle_shape_2d(...)` and `circle_shape_2d(...)`.
- Generated inline scripts, file-backed generated scripts, and referenced manual scripts.
- Direct `.tscn`, `.gd`, and `project.godot` emitters.
- Keyboard-only InputMap generation.
- Minimal display/window size settings.
- Build manifest at `.pygodot/manifest.json`.
- Generated/manual overwrite boundary.
- Snapshot tests.
- Examples:
  - `examples/minimal`
  - `examples/pong`
  - `examples/snake`
  - `examples/resources`
  - `examples/instancing`
  - `examples/timer`
  - `examples/audio`
  - `examples/font`
  - `examples/animation`
  - `examples/physics`

## Development rules for Codex

### General rules

- Keep changes small and milestone-focused.
- Do not add unrelated features while implementing a milestone.
- Do not rewrite the public DSL without explicit instruction.
- Preserve existing examples unless the milestone explicitly asks to change them.
- Preserve all existing tests and snapshots unless the change intentionally updates generated output.
- If generated output changes, update snapshots only after verifying the change is intentional.
- Prefer explicit, boring code over clever metaprogramming.
- Do not introduce context-manager DSL or metaclass DSL.
- Do not add broad generated wrappers for the entire Godot API.

### Public API rules

A new public helper or constructor may be added only when all are true:

1. It is needed by a concrete example or test.
2. It is documented or discoverable from `pygodot.__init__`.
3. It has direct unit coverage.
4. It does not duplicate a generic mechanism without adding clear ergonomic value.

Use `node(...)` for uncommon Godot nodes.

Add convenience constructors only for common, example-backed nodes.

### Testing rules

Every feature must have at least one of:

- direct unit test;
- emitter snapshot test;
- example build test;
- generated file assertion.

For generated output, prefer snapshot tests when the output is stable and readable.

Do not rely on Godot being installed for ordinary unit tests. Real Godot execution should be optional.

---

# Milestone 1 — Split and stabilize the test suite

## Goal

`tests/test_pipeline.py` has grown into a monolithic test file. Split it into focused modules before adding more features.

This milestone must not change production behavior.

## Tasks

Create focused test modules:

```text
tests/test_dsl_nodes.py
tests/test_values.py
tests/test_emitters_project.py
tests/test_emitters_tscn.py
tests/test_normalize.py
tests/test_validate.py
tests/test_build.py
tests/test_examples.py
tests/helpers.py
```

Move existing tests from `tests/test_pipeline.py` into the appropriate files.

Suggested mapping:

- `DslNodeTests` -> `tests/test_dsl_nodes.py`
- `ValueSerializationTests` -> `tests/test_values.py`
- project emitter tests -> `tests/test_emitters_project.py`
- `.tscn` emitter tests -> `tests/test_emitters_tscn.py`
- normalization tests -> `tests/test_normalize.py`
- validation tests -> `tests/test_validate.py`
- build tests -> `tests/test_build.py`
- example build/snapshot tests -> `tests/test_examples.py`
- helpers like `_load_example_game`, `_find_scene`, `_build_example_script`, `make_scene`, `assert_matches_snapshot` -> `tests/helpers.py`

## Acceptance criteria

- `python -m unittest discover -s tests` passes.
- No production files under `src/pygodot` are changed unless strictly necessary for imports.
- No snapshots change.
- Test names remain descriptive.
- Shared helper code does not import more than necessary.

## Anti-goals

- Do not add new pygodot features.
- Do not update examples.
- Do not rewrite tests into pytest unless explicitly requested.
- Do not introduce external test dependencies.

## Suggested Codex prompt

```text
Refactor the current test suite by splitting tests/test_pipeline.py into focused test modules.

Keep production behavior unchanged. Do not add new pygodot features.

Target structure:
- tests/test_dsl_nodes.py
- tests/test_values.py
- tests/test_emitters_project.py
- tests/test_emitters_tscn.py
- tests/test_normalize.py
- tests/test_validate.py
- tests/test_build.py
- tests/test_examples.py
- tests/helpers.py

Acceptance criteria:
- python -m unittest discover -s tests passes
- snapshots do not change
- src/pygodot remains unchanged unless strictly needed for imports
```

---

# Milestone 2 — Add API surface policy documentation

## Goal

Stop uncontrolled public API growth.

Add a short policy document explaining when to add public constructors/helpers and when to use generic `node(...)`.

## Tasks

Add:

```text
docs/API_SURFACE_POLICY.md
```

Document:

- what counts as public API;
- what counts as internal API;
- when a convenience constructor is justified;
- when generic `node(...)` should be used instead;
- required tests for new public API;
- requirement that examples justify new Godot surface;
- non-goals:
  - no full Godot API wrapper generation;
  - no metaclass/context-manager DSL;
  - no Python runtime;
  - no Python-to-GDScript transpiler.

Update `docs/ROADMAP.md` or README with a link to this document.

## Acceptance criteria

- `docs/API_SURFACE_POLICY.md` exists.
- README or roadmap links to it.
- The document explicitly says that new public helpers require tests and an example-backed use case.
- No production code changes are required.

## Anti-goals

- Do not remove existing public helpers.
- Do not rename existing public API.
- Do not generate wrappers.

## Suggested Codex prompt

```text
Add docs/API_SURFACE_POLICY.md describing pygodot public API growth rules.

The policy must explain when to add a convenience constructor, when to use node(...), what requires tests, and what remains out of scope.

Link it from docs/ROADMAP.md or README.md.

Do not change production code.
```

---

# Milestone 3 — Generic SubResource DSL

## Goal

Avoid adding every generated subresource as a one-off branch in the normalizer.

Currently `RectangleShape2D` is supported as a special DSL type. Keep that API, but introduce a generic internal/public mechanism for simple generated subresources.

## Target API

Preferred public shape:

```python
from pygodot import sub_resource, Vec2

shape = sub_resource(
    type="RectangleShape2D",
    id_hint="player_hitbox",
    size=Vec2(24, 32),
)
```

Existing wrapper should remain:

```python
from pygodot import rectangle_shape_2d, Vec2

shape = rectangle_shape_2d(size=Vec2(24, 32))
```

Add a new convenience wrapper backed by the generic mechanism:

```python
from pygodot import circle_shape_2d

shape = circle_shape_2d(radius=12)
```

## Design constraints

- `rectangle_shape_2d(...)` must remain backward-compatible.
- Internally, both rectangle and circle shape helpers should normalize through the same generic subresource path.
- IDs must be deterministic.
- The normalized model should still emit `IRSubResource`.
- Do not introduce a full generic Resource system yet.

## Tasks

1. Add DSL type/helper:
   - `SubResource`
   - `sub_resource(...)`
2. Rework `RectangleShape2D` / `rectangle_shape_2d(...)` to use or map into the generic mechanism.
3. Add:
   - `CircleShape2D`
   - `circle_shape_2d(radius=...)`
4. Export new helpers from:
   - `pygodot.dsl.__init__`
   - `pygodot.__init__`
5. Update normalizer to register generic subresources.
6. Update value validation if needed.
7. Add snapshot tests:
   - generic subresource property;
   - rectangle shape still unchanged or intentionally updated;
   - circle shape emission.
8. Add or update a small example if useful, but do not rewrite all examples.

## Acceptance criteria

- Existing `examples/physics` continues to build.
- Existing snapshots either remain unchanged or change only for intentional ID/format changes.
- `CollisionShape2D("Shape", shape=circle_shape_2d(radius=12))` emits:
  - `[sub_resource type="CircleShape2D" ...]`
  - `radius = 12`
  - `shape = SubResource(...)`
- Generic `sub_resource(...)` can emit a simple `.tscn` subresource.
- Tests cover ID determinism and deduplication behavior.

## Anti-goals

- Do not add many resource-specific helpers.
- Do not implement generated `.tres` yet.
- Do not introduce Godot-assisted emitter.
- Do not support arbitrary nested complex resources unless required by this milestone.

## Suggested Codex prompt

```text
Implement a generic SubResource DSL while preserving rectangle_shape_2d compatibility.

Add SubResource/sub_resource(...), rework rectangle_shape_2d to use the generic mechanism, and add circle_shape_2d(radius=...).

Update exports, normalization, validation, emitter tests, and snapshots.

Do not implement generated .tres files or a broad resource system.
```

---

# Milestone 4 — Flappy Bird v1 example

## Goal

Add the next small playable example that exercises the existing gameplay-oriented surface without requiring assets.

This should validate:

- `Area2D`;
- `CollisionShape2D`;
- generated shape subresources;
- `Timer`;
- input actions;
- signals;
- GDScript from source file;
- game state/restart;
- more complex but still simple scene hierarchy.

## Example structure

```text
examples/flappy/
  README.md
  game.py
  scripts/main.gd
```

## Scene structure

Recommended scene:

```text
Main: Node2D
  Background: ColorRect
  Bird: Area2D
    BirdVisual: ColorRect
    BirdShape: CollisionShape2D
  Ground: Area2D
    GroundVisual: ColorRect
    GroundShape: CollisionShape2D
  PipeTopA: Area2D
    PipeTopAVisual: ColorRect
    PipeTopAShape: CollisionShape2D
  PipeBottomA: Area2D
    PipeBottomAVisual: ColorRect
    PipeBottomAShape: CollisionShape2D
  PipeTopB: Area2D
    PipeTopBVisual: ColorRect
    PipeTopBShape: CollisionShape2D
  PipeBottomB: Area2D
    PipeBottomBVisual: ColorRect
    PipeBottomBShape: CollisionShape2D
  ScoreLabel: Label
  StateLabel: Label
  SpawnTimer: Timer
```

Keep v1 simple:

- no textures;
- no audio;
- no dynamic scene instancing;
- no generated `.tres`;
- rectangular visuals only;
- pipes can be reused/moved by script instead of spawned dynamically.

## Input actions

```python
game.add_input_action("flap", keys=["SPACE", "UP"])
game.add_input_action("restart", keys=["R"])
```

## Window

Recommended:

```python
game.set_window(size=Vec2(480, 720))
```

## GDScript expectations

`scripts/main.gd` should handle:

- gravity;
- flap impulse;
- pipe movement;
- pipe reset/reuse;
- score update;
- collision/game over;
- restart;
- simple state labels.

## Tests

Add:

- snapshot `tests/snapshots/flappy_scene.tscn`;
- snapshot `tests/snapshots/flappy_script.gd`;
- example build test verifying generated files;
- assertions for:
  - `Area2D`;
  - `CollisionShape2D`;
  - `Timer`;
  - `area_entered`;
  - `timeout`;
  - input action `flap`;
  - window size.

## Acceptance criteria

- `python examples/flappy/game.py` can run when Godot is available.
- `from examples.flappy.game import game; game.build()` works.
- Unit tests pass.
- Flappy v1 is playable enough:
  - Space/Up flaps;
  - pipes move;
  - collision ends the game;
  - R restarts.

## Anti-goals

- Do not add art assets.
- Do not add audio.
- Do not implement dynamic PackedScene spawning.
- Do not implement a physics abstraction layer.
- Do not add many new public constructors unless strictly needed.

## Suggested Codex prompt

```text
Add examples/flappy as a small playable Flappy Bird style example.

Use existing pygodot DSL features: Area2D, CollisionShape2D, ColorRect, Label, Timer, input actions, window settings, and Script.from_file.

Use rectangular visuals only. Do not add assets or audio. Do not add dynamic scene instancing.

Add snapshots and build tests for the example.
```

---

# Milestone 5 — Optional real Godot smoke runner

## Goal

Add a developer tool to run real Godot smoke checks for examples when Godot is available, without making ordinary unit tests depend on Godot.

## Tool

Add:

```text
tools/smoke_examples.py
```

Expected usage:

```bash
python tools/smoke_examples.py --examples minimal,pong,snake,timer,physics
python tools/smoke_examples.py --all
python tools/smoke_examples.py --all --frames 20
python tools/smoke_examples.py --all --require-godot
```

Behavior:

- imports selected example `game` objects;
- calls `game.check_run(frames=N)`;
- prints summary;
- if Godot is missing:
  - default: skip with clear message and exit 0;
  - with `--require-godot`: exit non-zero.

## Acceptance criteria

- The tool works without new third-party dependencies.
- The tool does not run during normal unit tests.
- README documents usage.
- It supports at least:
  - minimal;
  - pong;
  - snake;
  - timer;
  - physics;
  - flappy, if Milestone 4 is complete.

## Anti-goals

- Do not add GitHub Actions requirement yet.
- Do not make `python -m unittest discover -s tests` require Godot.
- Do not add complex reporting.

## Suggested Codex prompt

```text
Add tools/smoke_examples.py to run optional real Godot smoke checks for examples.

The tool should call game.check_run(frames=N) for selected examples. It must skip cleanly when Godot is unavailable unless --require-godot is passed.

Document usage in README. Do not make unit tests depend on Godot.
```

---

# Milestone 6 — Script templates without transpilation

## Goal

Improve GDScript ergonomics without turning Python into a GDScript transpiler.

Current options:

- inline generated script body;
- `Script.from_file(...)`;
- `Script.reference(...)`.

Add simple file template support for generated scripts.

## Target API

```python
Script.from_template(
    source="scripts/player.gd.tmpl",
    path="res://scripts/player.gd",
    extends="Node2D",
    context={
        "speed": 300,
        "jump_force": -420,
    },
)
```

## Template engine

Keep it simple.

Acceptable options:

- `string.Template`;
- `str.format_map`.

Do not add Jinja2 unless explicitly requested.

## Behavior

- Template source is resolved relative to `Game.source_root`.
- Missing template file should raise `BuildError`.
- Missing context variable should raise `BuildError` with:
  - script path;
  - source path;
  - missing key.
- Rendered body is emitted through existing `GdScriptEmitter`.

## Acceptance criteria

- `Script.from_file(...)` remains unchanged.
- `Script.reference(...)` remains unchanged.
- `Script.from_template(...)` works.
- Tests cover:
  - successful render;
  - missing file;
  - missing variable;
  - source path escaping rejection.
- Add one small example or update Flappy/Pong only if it makes the script clearer.

## Anti-goals

- Do not parse Python AST.
- Do not translate Python code into GDScript.
- Do not build a GDScript AST.
- Do not add external dependencies.

## Suggested Codex prompt

```text
Add Script.from_template(...) for simple generated GDScript templates.

Use a standard-library-only template mechanism. Resolve source relative to Game.source_root. Raise BuildError for missing files and missing template variables.

Do not implement Python-to-GDScript transpilation.
```

---

# Milestone 7 — Scene reference ergonomics

## Goal

Make generated scene instancing less stringly-typed.

Current pattern:

```python
game.add_scene(gem_scene)
gem_ref = packed_scene("res://scenes/gem.tscn")
scene_instance("GemA", gem_ref)
```

Preferred ergonomic addition:

```python
game.add_scene(gem_scene)
scene_instance("GemA", gem_scene.as_packed_scene())
```

## Tasks

1. Add `Scene.as_packed_scene() -> ExternalResource`.
2. Update `examples/instancing` to use it.
3. Keep `packed_scene(...)` unchanged.
4. Add tests.

## Acceptance criteria

- `Scene.as_packed_scene()` returns `ExternalResource(path=scene.path, type="PackedScene")`.
- Existing `packed_scene(...)` behavior remains unchanged.
- Instancing example still builds.
- Snapshot output should remain unchanged.

## Anti-goals

- Do not introduce a new ComponentScene class unless explicitly requested.
- Do not add automatic dependency registration beyond existing scene registration behavior.
- Do not change scene paths.

## Suggested Codex prompt

```text
Add Scene.as_packed_scene() as a small ergonomic helper for scene instances.

Update examples/instancing to use it. Keep packed_scene(...) working. Snapshot output should remain unchanged.
```

---

# Milestone 8 — Minimal generated `.tres` strategy

## Goal

Start generated `.tres` support narrowly and deliberately.

Do not implement a broad resource system yet.

## Candidate first resource

Prefer a UI-focused resource because it will be useful soon:

```text
LabelSettings
```

Possible API:

```python
title_settings = label_settings(
    path="res://ui/title_label_settings.tres",
    font_size=32,
    font_color=Color(1, 1, 1),
)

Label(
    "Title",
    text="Hello",
    label_settings=title_settings,
)
```

## Tasks

1. Add a minimal generated resource declaration model.
2. Add `TresEmitter`.
3. Extend `Game.build()` to write generated `.tres` files.
4. Track generated `.tres` files in manifest.
5. Add `label_settings(...)`.
6. Add example:
   - `examples/generated_tres`
7. Add snapshots:
   - generated `.tres`;
   - scene referencing generated `.tres`.

## Acceptance criteria

- Generated `.tres` is deterministic.
- Scene can reference generated `.tres` as `ExtResource`.
- Manifest records generated resource file.
- Existing copied `.tres` resources still work.

## Anti-goals

- Do not implement all Godot resource types.
- Do not switch simple scene subresources to external `.tres`.
- Do not introduce Godot-assisted resource generation yet.

## Suggested Codex prompt

```text
Implement a minimal generated .tres pipeline for LabelSettings only.

Add a TresEmitter, generated resource tracking in Game.build(), a label_settings(...) helper, and an example demonstrating a Label using generated LabelSettings.

Do not implement a broad resource system.
```

---

# Recommended execution order

Use this order unless the user explicitly says otherwise:

```text
1. Split test suite
2. Add API surface policy document
3. Generic SubResource DSL
4. Flappy Bird v1 example
5. Optional real Godot smoke runner
6. Script templates
7. Scene.as_packed_scene()
8. Minimal generated .tres strategy
```

## Why this order

- First stabilize tests and rules.
- Then generalize subresources before adding more physics/resource examples.
- Then add Flappy Bird as the next meaningful playable example.
- Then improve operational confidence with optional Godot smoke checks.
- Then improve script ergonomics.
- Then refine scene instancing ergonomics.
- Then start generated `.tres` support.

---

# Near-term non-goals

Do not implement these unless the user explicitly changes direction:

- Python runtime inside Godot.
- Python-to-GDScript transpiler.
- GDExtension Python integration.
- Full Godot API wrapper generation.
- Visual editor replacement.
- ECS.
- Broad physics DSL.
- Complete resource DSL for all Godot resources.
- Export presets and release packaging.
- Godot-assisted emitter.
- Complex UI layout framework.
- Asset pipeline beyond copying/generating resources required by examples.

---

# Definition of done for each milestone

A milestone is complete only when:

- relevant unit tests pass;
- generated output is deterministic;
- snapshots are updated only intentionally;
- README/docs are updated when public behavior changes;
- examples still build;
- no unrelated features are added;
- public API exports are updated if a new public helper is introduced.
