# API Surface Policy

This document describes when `pygodot` should grow its public Python API.

The project should stay explicit, typed where useful, and example-driven. A
small public surface is easier to document, test, and keep stable than a broad
wrapper for all of Godot.

## Public API

Public API is anything users are expected to import from `pygodot` or
`pygodot.dsl`, including:

- `Game`, `Scene`, `Script`, and public DSL dataclasses;
- node constructors such as `Node2D`, `Label`, `Timer`, and `Area2D`;
- resource helpers such as `texture(...)`, `packed_scene(...)`, and
  `rectangle_shape_2d(...)`;
- generated resource helpers such as `label_settings(...)` and
  `style_box_flat(...)`;
- value wrappers such as `Vec2`, `Color`, and `NodePath`;
- functions exported from `pygodot.__init__` or `pygodot.dsl.__init__`.

Public API must be kept backward-compatible unless the user explicitly approves
a breaking change.

## Stable For 0.1

Stable for 0.1 means the API name, broad purpose, and normal usage pattern
should not change without an explicit breaking-change decision. Exact generated
text remains test-protected, but small emitter formatting fixes may still happen
when they are intentional and snapshot-reviewed.

The stable 0.1 surface is:

- `Game`, including `build()`, `run()`, `check_run()`, `add_scene(...)`,
  `add_input_action(...)`, `add_autoload(...)`, `set_icon(...)`,
  `set_display(...)`, `set_project_setting(...)`, and `set_window(...)`;
- `BuildResult` and `GodotRunResult` as the structured results for build and
  smoke-check workflows;
- `Scene`;
- `Script`, including inline generated scripts, `Script.from_file(...)`,
  `Script.from_template(...)`, and `Script.reference(...)`;
- `Node` and generic `node(...)`;
- basic node constructors used by examples:
  `Node2D`, `Control`, `ColorRect`, `Label`, `Button`, `Sprite2D`, `Timer`,
  `AudioStreamPlayer`, `AnimationPlayer`, `Area2D`, and `CollisionShape2D`;
- scene instancing through `scene_instance(...)` and `Scene.as_packed_scene()`;
- signals through `SignalConnection` and `signal(...)`;
- value wrappers:
  `Vec2`, `Vec3`, `Rect2`, `Color`, and `NodePath`;
- external resource declarations:
  `ExternalResource`, `ext_resource(...)`, `external_resource(...)`,
  `texture(...)`, `audio_stream(...)`, `font(...)`, and `packed_scene(...)`;
- keyboard and mouse button InputMap declaration through
  `Game.add_input_action(..., keys=..., mouse_buttons=...)`;
- project-level autoload, icon, display stretch, and focused extra project
  settings declarations;
- minimal window sizing through `WindowSettings` and `Game.set_window(...)`;
- the library-first workflow where a user project imports `pygodot`, creates a
  `Game`, and calls methods on that object.

## Experimental Surface

Experimental means the API is public and tested, but still shaped by examples.
It should remain available during the 0.1 line when practical, yet its exact
shape may change with explicit documentation and tests as the resource model
settles.

The experimental surface is:

- generated `.tres` helpers:
  `GeneratedResource`, `label_settings(...)`, and `style_box_flat(...)`;
- generated animation helpers:
  `Animation`, `AnimationKey`, `ValueTrack`, `animation(...)`, `key(...)`, and
  `value_track(...)`;
- generic scene sub-resources:
  `SubResource` and `sub_resource(...)`;
- generated shape sub-resources:
  `RectangleShape2D`, `CircleShape2D`, `rectangle_shape_2d(...)`, and
  `circle_shape_2d(...)`;
- exact `.pygodot/manifest.json` JSON shape and ordering;
- generated resource registry details, resource IDs, and ownership internals
  beyond the documented generated/copied/referenced distinction;
- exact smoke-check diagnostic formatting, beyond including command, return
  code, stdout tail, stderr tail, and Godot log tail.
- broad use of `set_project_setting(...)` outside documented LD49-style
  project settings.

Experimental APIs must still follow the same test and documentation rules as
stable APIs when they are added or changed.

## Internal API

Internal API includes modules that implement normalization, validation,
emission, file writing, and Godot CLI integration:

- `pygodot.ir.*`;
- `pygodot.emitters.*`;
- private helper functions;
- build-manifest implementation details;
- test helpers under `tests/`.

Internal APIs may change when needed, but generated output should remain
deterministic and covered by tests.

## Adding Convenience Helpers

Add a new public helper or constructor only when all of these are true:

1. A concrete example or test needs it.
2. It improves ergonomics over `node(...)` or an existing generic helper.
3. It is exported from both `pygodot.dsl.__init__` and `pygodot.__init__`.
4. It has direct unit coverage.
5. Its generated output has a snapshot or build assertion when applicable.
6. The relevant docs mention the new surface.

Good candidates are common Godot concepts that appear repeatedly in examples,
such as `Timer`, `Area2D`, or a narrow resource helper.

## Using `node(...)`

Use generic `node(name, type, ...)` when a Godot class is uncommon, appears in
only one local experiment, or does not need special typing or behavior.

Prefer `node(...)` for:

- one-off Godot node classes;
- exploratory examples;
- nodes whose only benefit would be avoiding the `type` string;
- broad Godot API coverage without a specific example-backed reason.

If a `node(...)` use becomes repeated or awkward in real examples, it can
graduate into a convenience constructor later.

## Required Tests

New public API must have tests appropriate to its behavior:

- constructor/helper tests for public DSL objects;
- normalization tests when the helper maps to IR resources or references;
- emitter snapshots for deterministic generated text;
- example build tests when an example depends on the new surface.

Ordinary unit tests must not require a Godot binary. Real Godot checks should
remain optional smoke tests.

## Example-Backed Surface

Examples justify API growth. Add only the Godot surface needed by the current
example or milestone, then stop.

Do not add adjacent helpers merely because they are similar. For example, a
`CircleShape2D` milestone may justify `circle_shape_2d(...)`, but not a full
physics resource hierarchy.

## Non-Goals

The public API must not become:

- a generated wrapper for the entire Godot API;
- a metaclass or context-manager DSL;
- a Python runtime inside Godot;
- a Python-to-GDScript transpiler;
- a broad resource system before examples require it.
