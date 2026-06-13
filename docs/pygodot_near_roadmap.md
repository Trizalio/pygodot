# Near Roadmap

The Pong sprint is complete. The current near-term goal is to use the framework
on one more small game before adding larger abstractions.

## Baseline after Pong

The repository currently has:

- a minimal example under `examples/minimal`;
- a playable two-scene Pong example under `examples/pong`;
- generated menu and game scenes;
- generated GDScript;
- keyboard-only InputMap DSL;
- deterministic snapshots for generated scenes/scripts;
- Godot smoke checks through `Game.check_run(...)`;
- documented generated/manual ownership boundaries.

## Milestone A - Snake

Create `examples/snake` as the next non-trivial example.

Constraints:

- use one simple scene;
- prefer `_draw()` for rendering the board and snake;
- use InputMap actions for direction/restart;
- avoid physics bodies and collision resources;
- avoid Timer DSL unless the pain is clear;
- keep generated output snapshot-testable.

Expected files:

```text
examples/snake/
  game.py
  README.md
```

Generated output should remain ignored under:

```text
examples/snake/build/
```

Acceptance criteria:

- `game.build()` writes a normal Godot project;
- `game.check_run(frames=...)` succeeds when Godot is available;
- the game is playable in `game.run()`;
- snapshots cover the scene and generated script if the output is stable;
- no broad new DSL is introduced without pain from the example.

## Milestone B - Project Settings

After Snake, add only the project settings that examples need.

Likely first setting:

```python
game.set_window(size=Vec2(800, 600))
```

Do not add a broad settings API until examples justify it.

## Milestone C - Script Ergonomics

If generated script bodies become too large inside Python strings, add a narrow
script source feature:

```python
Script.from_file("scripts/snake.gd", path="res://scripts/snake.gd", extends="Node2D")
```

The generated/manual boundary must stay explicit.
