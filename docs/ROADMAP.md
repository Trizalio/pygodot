# Roadmap

This roadmap describes the current product direction. Completed sprint history
belongs in git.

## Current baseline

`pygodot` can generate and run small native Godot 4 projects from ordinary
Python code.

Implemented:

- library-first `Game` API with `build()`, `run()`, and `check_run()`;
- public scene/node/script DSL;
- generic `node(...)` helper and selected node constructors: `Node2D`,
  `Control`, `ColorRect`, `Sprite2D`, `Label`, `Button`, `Timer`,
  `AudioStreamPlayer`;
- typed value wrappers: `Vec2`, `Vec3`, `Rect2`, `Color`, `NodePath`;
- external resources through `ext_resource(...)`, `texture(...)`,
  `audio_stream(...)`, `font(...)`, and `packed_scene(...)`;
- scene instances through `scene_instance(...)`;
- generated, file-backed, and referenced GDScript;
- direct `.tscn`, `.gd`, and `project.godot` emitters;
- keyboard-only InputMap generation;
- minimal display/window size settings;
- build manifest at `.pygodot/manifest.json`;
- generated/manual overwrite boundary;
- deterministic snapshot tests;
- `examples/minimal`;
- a playable two-scene `examples/pong`;
- a draw-based `examples/snake`;
- a source-asset `examples/resources`;
- a generated PackedScene instancing `examples/instancing`;
- a signal-connected timer `examples/timer`;
- an audio resource `examples/audio`;
- a font resource `examples/font`.

## Next: script templates

Generated raw script bodies and `Script.from_file(...)` cover the current
examples. Larger examples may need a little more ergonomics:

- simple template support;
- clearer error reporting for generated GDScript smoke checks.

This is still not Python-to-GDScript transpilation.

## Next: richer examples

Pick the next small playable or visual example, then add only the Godot surface
that example needs.

Likely candidates:

- shape resources for physics examples;
- Godot-assisted emission for resources that are brittle to write by hand.

## Non-goals for the near term

- Python runtime inside Godot;
- Python-to-GDScript transpiler;
- generated wrappers for the entire Godot API;
- visual editor replacement;
- ECS;
- broad physics/resource DSL before examples justify it.
