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
  `Control`, `ColorRect`, `Label`, `Button`;
- typed value wrappers: `Vec2`, `Vec3`, `Rect2`, `Color`, `NodePath`;
- external resources through `ext_resource(...)`, `texture(...)`, and
  `packed_scene(...)`;
- generated and referenced GDScript;
- direct `.tscn`, `.gd`, and `project.godot` emitters;
- keyboard-only InputMap generation;
- minimal display/window size settings;
- build manifest at `.pygodot/manifest.json`;
- generated/manual overwrite boundary;
- deterministic snapshot tests;
- `examples/minimal`;
- a playable two-scene `examples/pong`;
- a draw-based `examples/snake`.

## Next: script sources and templates

Generated raw script bodies are enough for the current examples, but larger
examples will need better ergonomics:

- `Script.from_file(...)`;
- simple template support;
- clearer error reporting for generated GDScript smoke checks.

This is still not Python-to-GDScript transpilation.

## Later: richer resources

Delay complex Godot resources until an example needs them.

Likely candidates:

- `Timer`;
- scene instancing through `PackedScene`;
- shape resources for physics examples;
- Godot-assisted emission for resources that are brittle to write by hand.

## Non-goals for the near term

- Python runtime inside Godot;
- Python-to-GDScript transpiler;
- generated wrappers for the entire Godot API;
- visual editor replacement;
- ECS;
- broad physics/resource DSL before examples justify it.
