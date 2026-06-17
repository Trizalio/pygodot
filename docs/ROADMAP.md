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
  `AnimationPlayer`, `AudioStreamPlayer`, `Area2D`, `CollisionShape2D`, and
  narrow LD49-style Control/UI helpers;
- typed value wrappers: `Vec2`, `Vec3`, `Rect2`, `Color`, `NodePath`,
  `StringName`;
- external resources through `ext_resource(...)`, `texture(...)`,
  `audio_stream(...)`, `font(...)`, and `packed_scene(...)`;
- scene instances through `scene_instance(...)` and generated scene references
  through `Scene.as_packed_scene()`;
- generated value-track animations through `animation(...)`;
- generic generated scene sub-resources through `sub_resource(...)`;
- generated shape resources through `rectangle_shape_2d(...)` and
  `circle_shape_2d(...)`;
- generated `LabelSettings` `.tres` resources through `label_settings(...)`,
  including font references;
- generated `StyleBoxFlat` `.tres` resources through `style_box_flat(...)`;
- generated, file-backed, templated, and referenced GDScript;
- direct `.tscn`, `.gd`, `.tres`, and `project.godot` emitters;
- keyboard-only InputMap generation;
- minimal display/window size settings;
- build manifest at `.pygodot/manifest.json` with explicit resource ownership;
- generated/manual overwrite boundary;
- optional real Godot example smoke runner at `tools/smoke_examples.py`;
- deterministic snapshot tests;
- `examples/minimal`;
- a playable two-scene `examples/pong`;
- a draw-based `examples/snake`;
- a source-asset `examples/resources`;
- a generated PackedScene instancing `examples/instancing`;
- a signal-connected timer `examples/timer`;
- a templated generated script `examples/template_script`;
- an audio resource `examples/audio`;
- a font resource `examples/font`;
- a generated AnimationPlayer `examples/animation`;
- a 2D collision shape `examples/physics`;
- a small playable `examples/flappy`;
- a generated `.tres` `examples/generated_tres`;
- a static generated UI panel with reusable `.tres` styles in
  `examples/ui_panel`;
- an LD49-style Control/container menu shell in `examples/ld49_ui_shell`;
- an LD49-style autoload scene flow slice in `examples/ld49_scene_flow`;
- an LD49-style animated unit resource slice in `examples/ld49_unit_card`.

## Next Direction

Upcoming near-term work should stay library-first and example-backed. Use
`docs/NEXT_CODEX_ROADMAP.md` for the active Codex work plan; keep this file as
the short product-direction overview.

Likely candidates:

- clearer resource dependency boundaries;
- better Godot smoke-check error reporting;
- one small InputMap increment if an example needs it.

## Non-goals for the near term

- Python runtime inside Godot;
- Python-to-GDScript transpiler;
- generated wrappers for the entire Godot API;
- visual editor replacement;
- ECS;
- broad physics/resource DSL beyond examples that justify it.
