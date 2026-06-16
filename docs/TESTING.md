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
- generated script template rendering;
- manifest contents;
- Godot CLI command construction.

Unit tests must not require a Godot binary.

Run:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

## Continuous Integration

GitHub Actions runs the ordinary unit test suite on push and pull request using
Python 3.11. CI does not install Godot and does not run real Godot smoke checks.

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
- template script scene/script rendered from `string.Template`.
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
- existing external resources are copied and recorded in the manifest with
  explicit ownership;
- missing external resources remain referenced and visible in both
  `BuildResult.referenced_resources` and the manifest;
- generated `.tres` dependencies follow the same copied/referenced ownership
  rules as scene-level external resources;
- generated resources and referenced manual resources keep distinct manifest
  ownership;
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
python tools/smoke_examples.py --examples minimal,pong,snake,timer,template_script,physics,flappy
python tools/smoke_examples.py --all --frames 20
```

`check_run(...)` runs Godot headless for a fixed number of frames, captures logs,
and raises if Godot reports script or parse errors.

When a smoke check fails, the exception includes a concise diagnostic summary:

- command;
- return code;
- stdout tail;
- stderr tail;
- Godot log tail, when the log file exists.

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
