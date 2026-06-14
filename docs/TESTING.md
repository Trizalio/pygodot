# Testing Strategy

Generated output must be deterministic and easy to review.

## Unit Tests

Unit tests cover:

- value serialization;
- DSL constructors and helpers;
- DSL to IR normalization;
- validation errors;
- project, scene, and script emitters;
- generated/manual build behavior;
- manifest contents;
- Godot CLI command construction.

Unit tests must not require a Godot binary.

Run:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

## Snapshot Tests

File snapshots live under `tests/snapshots/`.

Current snapshots cover:

- a minimal `.tscn`;
- Pong menu scene;
- Pong game scene;
- generated Pong script.
- Snake scene;
- generated Snake script.
- resources scene with copied texture resource.
- instancing scenes with a generated `PackedScene` resource.
- timer scene/script with a built-in `timeout` signal connection.
- audio scene/script with a copied `AudioStream` resource.
- font scene with a copied `Font` resource.
- animation scene with generated `Animation` and `AnimationLibrary` sub-resources.
- physics scene/script with generated `RectangleShape2D` sub-resources.
- flappy scene/script with generated collision shapes, input actions, and timer
  signals.
- emitter and normalization coverage for generic generated sub-resources and
  `CircleShape2D`.

Snapshot tests protect:

- property ordering;
- external resource ordering;
- stable resource IDs;
- parent paths;
- signal connections;
- final newlines;
- absence of timestamps and absolute paths.

## Build Integration Tests

Build tests create temporary generated projects and verify:

- expected files are written;
- repeated builds are stable;
- manual script references are not written;
- existing external resources are copied and recorded in the manifest;
- unsafe `res://` paths are rejected.

## Godot Smoke Checks

When `GODOT_BIN` is available, examples can be checked with:

```powershell
$env:PYTHONPATH = "src"
python -c "from examples.pong.game import game; game.check_run(frames=20)"
```

Multiple examples can be checked with:

```powershell
$env:PYTHONPATH = "src"
python tools/smoke_examples.py --examples minimal,pong,snake,timer,physics,flappy
python tools/smoke_examples.py --all --frames 20
```

`check_run(...)` runs Godot headless for a fixed number of frames, captures logs,
and raises if Godot reports script or parse errors.

Godot smoke checks are useful before committing example changes, but they are
not required for normal unit test runs. The smoke runner skips cleanly when
Godot is unavailable unless `--require-godot` is passed.

## Validation Cases

Keep negative tests for:

- duplicate sibling names;
- invalid `res://` paths;
- unsupported property values;
- invalid generated/manual script ownership;
- invalid input action names and keys;
- duplicate input action names;
- unsafe generated paths;
- useful error context.
