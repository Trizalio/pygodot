# Near Roadmap

Pong and Snake are complete enough to show the current framework shape. The next
near-term work should remove pain that both examples now reveal.

## Baseline

The repository currently has:

- a minimal example under `examples/minimal`;
- a two-scene Pong example under `examples/pong`;
- a one-scene Snake example under `examples/snake`;
- generated GDScript gameplay;
- keyboard-only InputMap DSL;
- deterministic snapshots for example scenes/scripts;
- Godot smoke checks through `Game.check_run(...)`;
- documented generated/manual ownership boundaries.

## Milestone A - Minimal Project Settings

Add only the project settings that examples need.

First target:

```python
game.set_window(size=Vec2(800, 600))
```

Expected output:

- `project.godot` contains the relevant `[display]` window settings;
- Pong and Snake no longer rely only on script-local constants for their
  intended viewport;
- tests cover emitted `project.godot`;
- no broad settings DSL is introduced.

## Milestone B - Script Ergonomics

Snake makes the raw Python string body noticeably large. Add a narrow way to
load generated script bodies from source files while keeping ownership explicit.

Possible API:

```python
Script.from_file(
    source="scripts/snake.gd",
    path="res://scripts/snake.gd",
    extends="Node2D",
)
```

Acceptance criteria:

- source `.gd` files live under `source_root`;
- generated `.gd` files are still written into `build_dir`;
- manual `Script.reference(...)` remains distinct from generated script sources;
- snapshots remain deterministic.

## Milestone C - Example-Driven Resource Work

Do not add physics/resource abstractions yet. Pick the next example first, then
add only the resource support that example needs.
