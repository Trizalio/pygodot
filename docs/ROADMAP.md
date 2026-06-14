# Roadmap

This roadmap describes the current product direction. Completed sprint history
belongs in git.

## Current baseline

`pygodot` can generate and run small native Godot 4 projects from ordinary
Python code.

Implemented:

- library-first `Game` API with `build()`, `run()`, and `check_run()`;
- public scene/node/script DSL;
- documented public API surface policy in `docs/API_SURFACE_POLICY.md`;
- generic `node(...)` helper and selected node constructors: `Node2D`,
  `Control`, `ColorRect`, `Sprite2D`, `Label`, `Button`, `Timer`,
  `AnimationPlayer`, `AudioStreamPlayer`, `Area2D`, `CollisionShape2D`;
- typed value wrappers: `Vec2`, `Vec3`, `Rect2`, `Color`, `NodePath`;
- external resources through `ext_resource(...)`, `texture(...)`,
  `audio_stream(...)`, `font(...)`, and `packed_scene(...)`;
- scene instances through `scene_instance(...)`;
- generated value-track animations through `animation(...)`;
- generic generated scene sub-resources through `sub_resource(...)`;
- generated shape resources through `rectangle_shape_2d(...)` and
  `circle_shape_2d(...)`;
- generated, file-backed, templated, and referenced GDScript;
- direct `.tscn`, `.gd`, and `project.godot` emitters;
- keyboard-only InputMap generation;
- minimal display/window size settings;
- build manifest at `.pygodot/manifest.json`;
- generated/manual overwrite boundary;
- optional real Godot example smoke runner at `tools/smoke_examples.py`;
- deterministic snapshot tests;
- `examples/minimal`;
- a playable two-scene `examples/pong`;
- a draw-based `examples/snake`;
- a source-asset `examples/resources`;
- a generated PackedScene instancing `examples/instancing`;
- a signal-connected timer `examples/timer`;
- an audio resource `examples/audio`;
- a font resource `examples/font`;
- a generated AnimationPlayer `examples/animation`;
- a 2D collision shape `examples/physics`;
- a small playable `examples/flappy`.

## Next: ergonomics

Upcoming near-term work should stay library-first and example-backed. Script
templates are deliberately small and do not change the runtime strategy: this
is still not Python-to-GDScript transpilation.

## Next: richer examples

Pick the next small playable or visual example, then add only the Godot surface
that example needs.

Likely candidates:

- direct or Godot-assisted `.tres` resources that examples justify.

## Non-goals for the near term

- Python runtime inside Godot;
- Python-to-GDScript transpiler;
- generated wrappers for the entire Godot API;
- visual editor replacement;
- ECS;
- broad physics/resource DSL beyond examples that justify it.
