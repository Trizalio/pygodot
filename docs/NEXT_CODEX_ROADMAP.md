# pygodot: Next Development Roadmap for Codex

This document is the working roadmap for the next pygodot development
iterations. Completed sprint history belongs in git, not in this file.

Follow the milestones in order unless the user explicitly asks otherwise.

## Current Project Baseline

`pygodot` is a build-time Python library for declaring Godot 4 projects and
generating normal Godot project files.

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
- Scene instances through `scene_instance(...)` and generated scene references
  through `Scene.as_packed_scene()`.
- Generated value-track animations through `animation(...)`.
- Generic generated scene sub-resources through `sub_resource(...)`.
- Generated shape resources through `rectangle_shape_2d(...)` and
  `circle_shape_2d(...)`.
- Generated `LabelSettings` `.tres` resources through `label_settings(...)`.
- Generated inline scripts, file-backed generated scripts, templated generated
  scripts, and referenced manual scripts.
- Direct `.tscn`, `.gd`, `.tres`, and `project.godot` emitters.
- Keyboard-only InputMap generation.
- Minimal display/window size settings.
- Build manifest at `.pygodot/manifest.json`.
- Generated/manual overwrite boundary.
- Optional real Godot example smoke runner at `tools/smoke_examples.py`.
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
  - `examples/flappy`
  - `examples/generated_tres`

## Development Rules For Codex

- Keep changes small and milestone-focused.
- Do not add unrelated features while implementing a milestone.
- Do not rewrite the public DSL without explicit instruction.
- Preserve existing examples unless the milestone explicitly asks to change them.
- Preserve all existing tests and snapshots unless the change intentionally
  updates generated output.
- If generated output changes, update snapshots only after verifying the change
  is intentional.
- Prefer explicit, boring code over clever metaprogramming.
- Do not introduce context-manager DSL or metaclass DSL.
- Do not add broad generated wrappers for the entire Godot API.

## Public API Rules

A new public helper or constructor may be added only when all are true:

1. It is needed by a concrete example or test.
2. It is documented or discoverable from `pygodot.__init__`.
3. It has direct unit coverage.
4. It does not duplicate a generic mechanism without adding clear ergonomic
   value.

Use `node(...)` for uncommon Godot nodes. Add convenience constructors only for
common, example-backed nodes.

## Testing Rules

Every feature must have at least one of:

- direct unit test;
- emitter snapshot test;
- example build test;
- generated file assertion.

For generated output, prefer snapshot tests when the output is stable and
readable.

Do not rely on Godot being installed for ordinary unit tests. Real Godot
execution should be optional.

---

# Milestone 9 - UI Panel Example

## Goal

Add a small UI-focused example that uses the current DSL surface to build a
realistic static panel/HUD screen.

The purpose is to exercise generated `LabelSettings` in a more realistic scene
before adding more resource types.

## Example Structure

```text
examples/ui_panel/
  README.md
  game.py
```

## Suggested Scene

Use existing primitives first:

- `Control` as root;
- `ColorRect` for background and panel blocks;
- `Label` for title, section labels, and values;
- `Button` for actions;
- generated `LabelSettings` for title and section typography;
- optional generic `node(...)` only if a common Godot UI node is clearly useful.

Recommended window:

```python
game.set_window(size=Vec2(720, 480))
```

## Tasks

1. Add `examples/ui_panel`.
2. Use at least two generated `LabelSettings` resources.
3. Keep the example static unless a tiny script is clearly useful.
4. Add scene and `.tres` snapshots.
5. Add an example build test.
6. Add the example to `tools/smoke_examples.py`.
7. Update docs if the example reveals a recommended UI pattern.

## Acceptance Criteria

- `python -m unittest discover -s tests` passes.
- `python tools/smoke_examples.py --examples ui_panel --frames 1` passes when
  Godot is available.
- The generated scene references generated `.tres` files as `ExtResource`.
- The example does not add broad UI abstractions.

## Anti-Goals

- Do not add a layout framework.
- Do not add generated `Theme` support yet.
- Do not add many UI node constructors unless the example proves a repeated
  need.
- Do not add assets.

## Suggested Codex Prompt

```text
Add examples/ui_panel as a static UI-focused example.

Use existing Control, ColorRect, Label, Button, Vec2, Color, and generated
label_settings(...) resources. Add snapshots and a build test. Add the example
to tools/smoke_examples.py.

Do not add a layout framework or generated Theme support.
```

---

# Milestone 10 - Generated LabelSettings Font References

## Goal

Make generated `LabelSettings` useful with real font assets.

Current `label_settings(...)` supports size and color only. A common real-world
case is:

```python
title_settings = label_settings(
    "res://ui/title_label_settings.tres",
    font=font("res://assets/display.ttf"),
    font_size=36,
    font_color=Color(1, 1, 1),
)
```

The generated `.tres` should include an external font resource and assign it to
the `font` property.

## Tasks

1. Extend `label_settings(...)` with an optional `font` argument.
2. Teach `TresEmitter` to emit `.tres` external resources for generated
   resource properties that reference `ExternalResource`.
3. Keep `.tscn` external resource collection unchanged for scenes.
4. Ensure `Game.build()` still copies source-owned font assets referenced by a
   generated `.tres`.
5. Add unit and build tests.
6. Update `examples/ui_panel` or `examples/generated_tres` to demonstrate the
   real font case if a font asset is already available in the repository.

## Acceptance Criteria

- Generated `.tres` can contain `[ext_resource ...]` entries.
- Generated `.tres` can set `font = ExtResource(...)`.
- Font assets referenced only from generated `.tres` are copied and recorded in
  the manifest.
- Existing copied `.tres` resources still work.
- Existing scene snapshots remain unchanged unless intentionally updated.

## Anti-Goals

- Do not implement arbitrary nested resources.
- Do not add generated `Theme` support.
- Do not introduce Godot-assisted resource generation.
- Do not add new font assets if an existing example asset can be reused.

## Suggested Codex Prompt

```text
Extend generated LabelSettings resources so label_settings(...) can reference a
Font external resource.

TresEmitter should emit deterministic ext_resource entries inside .tres files
and Game.build() should copy font assets referenced from generated .tres files.
Keep the scope limited to LabelSettings font references.
```

---

# Milestone 11 - Generated StyleBoxFlat Resource

## Goal

Add one more UI-focused generated `.tres` resource only if the UI panel example
shows clear need for reusable panel/button styling.

Candidate API:

```python
panel_style = style_box_flat(
    "res://ui/panel_style.tres",
    bg_color=Color(0.08, 0.1, 0.12),
    border_color=Color(0.3, 0.45, 0.55),
    border_width_all=2,
    corner_radius_all=6,
)
```

Then a UI node can reference it through normal properties such as:

```python
node(
    "Panel",
    "PanelContainer",
    theme_override_styles={"panel": panel_style},
)
```

## Tasks

1. Add a narrow generated resource helper for `StyleBoxFlat`.
2. Reuse the generated `.tres` pipeline from `LabelSettings`.
3. Add emitter coverage for the specific supported properties only.
4. Update or add a UI example that demonstrates the resource.
5. Add snapshots and build tests.

## Acceptance Criteria

- Generated `StyleBoxFlat` is deterministic.
- A scene can reference it as `ExtResource`.
- Manifest records the generated resource file.
- Existing `LabelSettings` behavior remains unchanged.

## Anti-Goals

- Do not implement full `Theme` generation.
- Do not support every `StyleBoxFlat` property.
- Do not add broad resource polymorphism unless the existing generated resource
  model already handles it cleanly.

## Suggested Codex Prompt

```text
Add a narrow generated StyleBoxFlat .tres helper for UI styling.

Keep the supported property set small and example-backed. Reuse the existing
generated resource pipeline and add snapshots/build tests.
```

---

# Milestone 12 - Build Manifest Resource Ownership Polish

## Goal

Make the manifest clearer now that resources can be copied, generated, or
referenced without being copied.

Current manifest records generated files, generated scripts/scenes/resources,
and external resources with `copied: true/false`. This is workable but a little
ambiguous as generated resources grow.

## Tasks

1. Review the manifest shape after Milestones 9-11.
2. Decide whether external resource records need an explicit `ownership` or
   `source` field, such as:
   - `generated`
   - `copied`
   - `referenced`
3. If changed, update serialization tests and docs.
4. Preserve deterministic ordering.

## Acceptance Criteria

- Manifest output clearly distinguishes copied, generated, and referenced
  resources.
- Existing generated/manual overwrite boundaries remain intact.
- Tests cover the new manifest shape.

## Anti-Goals

- Do not build cleanup/pruning behavior yet.
- Do not change build directory ownership policy.
- Do not add a persistent mixed Godot project mode.

## Suggested Codex Prompt

```text
Polish the build manifest resource ownership model so copied, generated, and
referenced resources are clearly distinguishable.

Keep deterministic ordering and update tests/docs. Do not add cleanup behavior
or persistent project output mode.
```

---

# Recommended Execution Order

Use this order unless the user explicitly says otherwise:

```text
9. UI Panel example
10. Generated LabelSettings font references
11. Generated StyleBoxFlat resource
12. Build manifest resource ownership polish
```

## Why This Order

- First use the current generated `.tres` support in a more realistic UI example.
- Then extend only the proven `LabelSettings` use case with real font references.
- Then add one more UI resource if the example justifies it.
- Then polish manifest semantics once generated/copy/reference cases are all
  exercised.

---

# Near-Term Non-Goals

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

# Definition Of Done For Each Milestone

A milestone is complete only when:

- relevant unit tests pass;
- generated output is deterministic;
- snapshots are updated only intentionally;
- docs are updated when public behavior changes;
- examples still build;
- optional real Godot smoke checks pass when the task touches examples;
- no unrelated features are added;
- public API exports are updated if a new public helper is introduced.
