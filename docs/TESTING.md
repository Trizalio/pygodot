# Testing Strategy

Generated output must be deterministic and easy to review.

## Test categories

### Unit tests

Target:
- value serialization;
- path normalization;
- resource ID generation;
- node tree validation;
- signal validation;
- DSL to IR normalization.

### Snapshot tests

Target:
- `.tscn` emission;
- `.gd` emission;
- `project.godot` emission.

Snapshot tests are important because generated file format stability is a product feature.

### Integration tests

Target:
- build a minimal project into a temporary directory;
- verify expected files exist;
- verify copied external assets and `.pygodot/manifest.json`;
- optionally run Godot headless import if `GODOT_BIN` is available.

Godot-dependent tests should be skippable when Godot is not installed.

## Determinism requirements

The same input must produce the same output.

Test:
- run build twice;
- compare file contents;
- assert no unstable IDs/order/timestamps in generated files.

## Validation test cases

Required negative cases:
- empty node name;
- duplicate sibling names;
- invalid `res://` path;
- unsupported property value type;
- invalid script path;
- invalid signal method name;
- attempt to overwrite manual file.
- asset manifest contains stable generated/resource entries.
- validation errors include scene/node/property or resource context.
- unsafe `res://` paths cannot escape the generated project root.

## Snapshot example

A minimal scene should snapshot to a known `.tscn` text file.

Example logical input:

```python
Scene(
    path="res://scenes/main.tscn",
    root=Node2D("Main", children=[Label("Title", text="Hello")]),
)
```

Expected output should be stable:

```text
[gd_scene format=3]

[node name="Main" type="Node2D"]

[node name="Title" type="Label" parent="."]
text = "Hello"
```

## Godot validation

When Godot is available, run:

```bash
godot --headless --path <generated_project> --import
```

This should be an optional integration step, not a requirement for unit tests.

## Do not over-test implementation details

Prefer tests for:
- emitted output;
- public API behavior;
- validation errors.

Avoid tests that lock internal private helper structure too early.
