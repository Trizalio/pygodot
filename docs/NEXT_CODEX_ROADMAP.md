# pygodot: Next Codex Roadmap

This document is the active roadmap for upcoming `pygodot` development.

It is intended to be read by Codex before making project changes. Keep it current and focused on work that has not been completed yet. Completed sprint history belongs in git commits, not in this file.

Follow the milestones in order unless the user explicitly changes direction.

---

## 1. Current Baseline

`pygodot` is a build-time Python library for declaring Godot 4 projects and generating ordinary Godot project files.

Core principles that must remain unchanged:

- Python is used at build time only.
- Runtime logic remains ordinary GDScript.
- Do not introduce Python runtime inside Godot.
- Do not build a Python-to-GDScript transpiler.
- Do not introduce JSON/YAML as the main intermediate representation.
- Keep the internal pipeline as: Python DSL -> normalized IR -> emitters.
- Prefer direct `.tscn`, `.gd`, `.tres`, and `project.godot` emitters where practical.
- Keep generated output deterministic and snapshot-testable.
- Prefer library-first usage through `Game`, not command-line-only workflows.
- Keep API growth example-backed and intentionally narrow.

Current implemented surface includes:

- `Game.build()`, `Game.run()`, `Game.check_run()`.
- Explicit scene/node/script DSL.
- Selected node constructors plus generic `node(...)`.
- Typed values:
  - `Vec2`
  - `Vec3`
  - `Rect2`
  - `Color`
  - `NodePath`
- External resource helpers:
  - `ext_resource(...)`
  - `texture(...)`
  - `audio_stream(...)`
  - `font(...)`
  - `packed_scene(...)`
- Scene instances through `scene_instance(...)`.
- Generated scene references through `Scene.as_packed_scene()`.
- Generated value-track animations through `animation(...)`.
- Generic scene sub-resources through `sub_resource(...)`.
- Generated shape sub-resources:
  - `rectangle_shape_2d(...)`
  - `circle_shape_2d(...)`
- Generated `.tres` resources:
  - `label_settings(...)`, including font references;
  - `style_box_flat(...)`.
- Generated inline GDScript.
- File-backed generated GDScript through `Script.from_file(...)`.
- Templated generated GDScript through `Script.from_template(...)`.
- Referenced manual scripts through `Script.reference(...)`.
- Direct `.tscn`, `.gd`, `.tres`, and `project.godot` emitters.
- Keyboard-only InputMap generation.
- Minimal display/window size settings.
- Build manifest at `.pygodot/manifest.json` with explicit resource ownership.
- Generated/manual overwrite boundary.
- Optional real Godot example smoke runner at `tools/smoke_examples.py`.
- Deterministic snapshot tests.
- Minimal GitHub Actions unit-test CI that does not require Godot.
- User-facing README with capability matrix and example list.

Current examples include:

- `examples/minimal`
- `examples/pong`
- `examples/snake`
- `examples/resources`
- `examples/instancing`
- `examples/timer`
- `examples/template_script`
- `examples/audio`
- `examples/font`
- `examples/animation`
- `examples/physics`
- `examples/flappy`
- `examples/generated_tres`
- `examples/ui_panel`

---

## 2. Development Rules For Codex

Follow these rules for every task:

- Keep changes small and milestone-focused.
- Do not add unrelated features while implementing a milestone.
- Do not rewrite the public DSL unless explicitly requested.
- Preserve existing examples unless the milestone explicitly asks to change them.
- Preserve existing tests and snapshots unless generated output intentionally changes.
- If generated output changes, update snapshots only after verifying the change is intentional.
- Prefer explicit, boring code over clever metaprogramming.
- Do not introduce context-manager DSL or metaclass DSL.
- Do not add broad generated wrappers for the entire Godot API.
- Keep public API additions documented, exported, and tested.
- Ordinary unit tests must not require a Godot binary.
- Real Godot execution must remain optional.
- If a task touches examples, keep `tools/smoke_examples.py` up to date.

---

## 3. Public API Rules

A new public helper or constructor may be added only when all are true:

1. It is needed by a concrete example or test.
2. It improves ergonomics over `node(...)` or an existing generic helper.
3. It is exported from both `pygodot.dsl.__init__` and `pygodot.__init__`.
4. It has direct unit coverage.
5. Generated output has a snapshot or build assertion when applicable.
6. Relevant docs mention the new surface.

Use `node(...)` for uncommon Godot nodes. Add convenience constructors only for common, example-backed nodes.

Do not add adjacent helpers merely because they are similar.

---

## 4. Testing Rules

Every feature must have at least one of:

- direct unit test;
- normalization test;
- validation test;
- emitter snapshot test;
- example build test;
- generated file assertion.

For generated output, prefer snapshot tests when the output is stable and readable.

Ordinary test command:

```bash
python -m unittest discover -s tests
```

Optional smoke checks when Godot is available:

```bash
python tools/smoke_examples.py --examples <example_name> --frames 20
```

or:

```bash
python tools/smoke_examples.py --examples <example_name> --frames 20 --require-godot
```

---

# Milestone 1 - External Project Build Smoke Test

## Goal

Verify that `pygodot` works as an installed Python library from a project outside the repository checkout.

Current examples are useful, but they mostly exercise repository-local workflows. The next important product check is an external project scenario:

```text
pip install -e /path/to/pygodot
mkdir my_game
python game.py
```

This milestone must not require a real Godot binary.

## Tasks

1. Add a unit test that creates a temporary project directory outside the repository tree.
2. Write a tiny external `game.py` or construct the external project directly in the test.
3. Import `pygodot` as an installed package.
4. Create a `Game` with:
   - one scene;
   - one generated script;
   - one generated `.tres` resource if practical;
   - optionally one copied asset if the test remains simple.
5. Call `game.build()`.
6. Assert that build output contains:
   - `project.godot`;
   - generated scene;
   - generated script;
   - generated `.tres` if included;
   - `.pygodot/manifest.json`.
7. Assert manifest ownership for generated/copied/referenced resources used by the test.
8. Add a short README or docs note about using `pygodot` from an external project.

## Acceptance Criteria

- The test does not require `GODOT_BIN`.
- The test passes in GitHub Actions.
- The temporary project is outside the repository root.
- The test does not rely on `PYTHONPATH=src` as the only usage mode.
- No new public API is added.
- Existing generated output snapshots do not change unless intentionally needed.
- `python -m unittest discover -s tests` passes.

## Anti-Goals

- Do not add new Godot features.
- Do not add CLI workflows.
- Do not require Godot in CI.
- Do not publish to PyPI.
- Do not introduce a project template system yet.

## Suggested Codex Prompt

```text
Add an external-project build smoke test.

Create a unit test that builds a tiny pygodot project in a temporary directory outside the repository tree. The test should import pygodot as an installed package, create a Game with one scene, one generated script, and one generated resource if practical, call game.build(), and assert generated project.godot, scene, script, manifest, and resource ownership.

Do not require Godot.
Do not add new public API.
Do not change generated output unless necessary.
python -m unittest discover -s tests must pass.
```

---

# Milestone 2 - Package Metadata Hardening For 0.1.x

## Goal

Prepare the project for a first technical package release line.

The current project already has a broad public API and examples. Package metadata should communicate the project status and make editable installs/builds reliable.

## Tasks

1. Review `pyproject.toml`.
2. Decide whether to keep `version = "0.0.0"` or move to `0.1.0`.
3. Add or improve package metadata:
   - authors;
   - project URLs;
   - classifiers;
   - license metadata;
   - keywords if useful.
4. Ensure editable install works:

```bash
python -m pip install -e .
```

5. Optionally add a build check using `python -m build` if adding `build` as a dev tool is acceptable.
6. Document install-from-checkout usage in README or `docs/GETTING_STARTED.md`.

## Acceptance Criteria

- `python -m pip install -e .` works.
- CI still passes.
- Package metadata reflects that this is an early project.
- No PyPI publishing automation is added.
- No Godot dependency is added to Python package metadata.
- No runtime dependency is added unless strictly needed.

## Anti-Goals

- Do not publish to PyPI.
- Do not add release automation.
- Do not add a complex dependency manager.
- Do not require Godot in CI.
- Do not add packaging for generated Godot exports.

## Suggested Codex Prompt

```text
Harden pyproject.toml metadata for an early 0.1.x technical release.

Keep packaging simple and setuptools-based. Ensure editable install works. Add reasonable metadata such as authors, URLs, classifiers, and status. Do not add PyPI publishing, release automation, or Godot as a Python dependency.

python -m unittest discover -s tests must pass.
```

---

# Milestone 3 - Godot Smoke Diagnostics Polish

## Goal

Make `Game.check_run()` and `tools/smoke_examples.py` failures easier to diagnose.

The project now has many examples and optional real Godot checks. When a smoke check fails, the output should show enough information to debug without manually digging through generated logs.

## Tasks

1. Review `GodotRunResult` and smoke runner output.
2. Add a small diagnostic summary for failed runs:
   - command;
   - return code;
   - stdout tail;
   - stderr tail;
   - Godot log tail if available.
3. Keep successful smoke output short.
4. Add tests using mocked subprocess results and fake log files.
5. Update `docs/TESTING.md` or README if the user-facing command output changes.

## Acceptance Criteria

- Ordinary unit tests do not require Godot.
- Failed smoke checks include command, return code, stderr tail, and log tail.
- Successful smoke checks remain concise.
- Existing `Game.check_run()` behavior stays backward-compatible unless explicitly approved.
- `python -m unittest discover -s tests` passes.

## Anti-Goals

- Do not make Godot mandatory in CI.
- Do not add editor integration.
- Do not parse all Godot errors structurally.
- Do not introduce a logging framework.

## Suggested Codex Prompt

```text
Improve optional Godot smoke diagnostics.

When Game.check_run() or tools/smoke_examples.py fails, show a concise diagnostic summary with command, return code, stderr tail, stdout tail, and Godot log tail if present.

Use mocked subprocess/log tests. Do not require Godot in unit tests or CI.
```

---

# Milestone 4 - Public API Stability Markers

## Goal

Separate the relatively stable 0.1 API from experimental helpers.

The public surface is now large enough that users and future changes need a stability policy.

## Suggested Documentation

Update `docs/API_SURFACE_POLICY.md` with sections like:

```text
Stable for 0.1:
- Game
- BuildResult
- Scene
- Script
- Node
- node(...)
- basic node constructors
- Vec2, Vec3, Rect2, Color, NodePath
- external resource helpers
- build/run/check_run workflow

Experimental:
- generated .tres helpers
- animation helpers
- generic sub_resource(...)
- exact manifest JSON shape
- exact generated resource registry internals
```

The exact classification can differ, but it must be explicit.

## Tasks

1. Update `docs/API_SURFACE_POLICY.md`.
2. Optionally add short notes in README.
3. Do not remove or rename existing public API.
4. If necessary, add docstrings or comments for experimental helpers.

## Acceptance Criteria

- The stability status of major public APIs is documented.
- Experimental APIs are marked but remain available.
- No production behavior changes are required.
- `python -m unittest discover -s tests` passes.

## Anti-Goals

- Do not break public API.
- Do not add deprecation machinery.
- Do not remove experimental helpers.
- Do not add semantic versioning automation.

## Suggested Codex Prompt

```text
Document public API stability markers.

Update docs/API_SURFACE_POLICY.md to distinguish stable-for-0.1 API from experimental helpers. Do not remove or rename existing public API. No production behavior changes are required.
```

---

# Milestone 5 - Manifest Contract Documentation And Tests

## Goal

Formalize `.pygodot/manifest.json` as a useful build artifact.

The manifest already records generated files, generated resources, generated scenes, generated scripts, external resources, `copied`, and `ownership`. This should be documented and covered by a mixed-project contract test.

## Tasks

1. Create `docs/MANIFEST.md` or extend `docs/GENERATED_BOUNDARY.md`.
2. Document manifest fields:
   - `generated_files`;
   - `generated_scenes`;
   - `generated_scripts`;
   - `generated_resources`;
   - `external_resources`;
   - `copied`;
   - `ownership`.
3. Document allowed ownership values:
   - `generated`;
   - `copied`;
   - `referenced`.
4. Add or improve a test with a mixed project containing:
   - generated scene;
   - generated script;
   - generated `.tres`;
   - copied external asset;
   - referenced manual script or resource.
5. Assert deterministic ordering.

## Acceptance Criteria

- Manifest shape is documented.
- Ownership values are documented.
- A mixed-project test verifies manifest output.
- Existing generated/manual overwrite boundaries remain intact.
- `python -m unittest discover -s tests` passes.

## Anti-Goals

- Do not add cleanup/pruning behavior.
- Do not add persistent project output mode.
- Do not introduce a stateful manifest database.
- Do not change build directory ownership policy.

## Suggested Codex Prompt

```text
Document and test the build manifest contract.

Add docs for .pygodot/manifest.json fields and ownership values. Add a mixed-project manifest test covering generated scene, generated script, generated .tres, copied asset, and referenced manual resource/script.

Do not add cleanup behavior or persistent project output mode.
```

---

# Milestone 6 - InputMap Mouse Button Increment

## Goal

Extend InputMap only by one small, example-backed step beyond keyboard support.

Current InputMap support is keyboard-only. Add mouse button support only if paired with a small example.

## Candidate API

```python
game.add_input_action(
    "shoot",
    keys=["SPACE"],
    mouse_buttons=["LEFT"],
)
```

or, if preserving the current method signature is preferred, add a new explicit method:

```python
game.add_mouse_input_action("shoot", buttons=["LEFT"])
```

Prefer the design that least disrupts current keyboard users.

## Example

Add a tiny `examples/mouse_input`:

```text
examples/mouse_input/
  README.md
  game.py
  scripts/main.gd
```

Behavior:

- small scene with a marker and label;
- left click increments a counter or moves the marker;
- no assets;
- no new large gameplay system.

## Tasks

1. Extend the DSL/IR for input actions to include mouse buttons.
2. Extend `ProjectEmitter` to emit deterministic `InputEventMouseButton`.
3. Add validation for supported mouse buttons.
4. Keep keyboard behavior unchanged.
5. Add example and snapshots/build assertions.
6. Add the example to README and `tools/smoke_examples.py`.

## Acceptance Criteria

- Existing keyboard InputMap snapshots remain unchanged unless intentionally affected.
- Mouse input action emits deterministic `project.godot`.
- Unsupported mouse button names produce clear validation errors.
- `examples/mouse_input` builds.
- `python -m unittest discover -s tests` passes.

## Anti-Goals

- Do not implement full input abstraction.
- Do not add gamepad support.
- Do not add touch/gesture support.
- Do not add every Godot input event type.
- Do not make a large new game example.

## Suggested Codex Prompt

```text
Add one small example-backed InputMap increment: mouse button support.

Keep existing keyboard behavior unchanged. Add deterministic InputEventMouseButton emission, validation, tests, and a tiny examples/mouse_input that increments a counter or moves a marker on left click.

Do not add gamepad, touch, gestures, or a full input abstraction layer.
```

---

# Milestone 7 - Getting Started Tutorial

## Goal

Add a first-user tutorial that starts outside the repository examples.

Create:

```text
docs/GETTING_STARTED.md
```

The tutorial should show a user how to create a tiny game project from an empty folder using `pygodot` as an installed package.

## Tutorial Scope

Cover:

1. Install from checkout:

```bash
python -m pip install -e /path/to/pygodot
```

2. Create a new external project directory.
3. Write `game.py`.
4. Build the project.
5. Run the project if Godot is available.
6. Inspect generated output.
7. Add a script from file.
8. Add one asset or generated `.tres` resource.
9. Run optional smoke check.

## Acceptance Criteria

- Tutorial does not depend on `examples/`.
- Tutorial uses the public API only.
- Tutorial stays short enough to follow.
- README links to it.
- `python -m unittest discover -s tests` passes.

## Anti-Goals

- Do not document every API.
- Do not introduce new features.
- Do not require Godot for the build-only path.
- Do not make this a full game development guide.

## Suggested Codex Prompt

```text
Add docs/GETTING_STARTED.md.

It should guide a first user through installing pygodot from checkout, creating an external project folder, writing a small game.py, building a Godot project, optionally running it, adding a file-backed script, and optionally using a generated .tres resource.

Use only existing public API. Keep it concise and link it from README.
```

---

# Recommended Execution Order

Use this order unless the user explicitly says otherwise:

```text
1. External project build smoke test
2. Package metadata hardening for 0.1.x
3. Godot smoke diagnostics polish
4. Public API stability markers
5. Manifest contract documentation and tests
6. InputMap mouse button increment, only if still desired
7. Getting Started tutorial
```

## Why This Order

- First verify the real product scenario: using `pygodot` as an installed library in another project.
- Then harden package metadata around that usage model.
- Then improve diagnostics for optional real Godot checks.
- Then document API stability before the surface grows further.
- Then formalize the manifest contract.
- Then add one small input feature if a concrete example still justifies it.
- Finally add a Getting Started tutorial once the external-project workflow is tested.

---

# Standing Non-Goals

Do not implement these unless the user explicitly changes direction:

- Python runtime inside Godot.
- Python-to-GDScript transpiler.
- GDExtension Python integration.
- Full Godot API wrapper generation.
- Visual editor replacement.
- ECS.
- Broad physics DSL.
- Complete resource DSL for all Godot resources.
- Export presets and release packaging.
- Godot-assisted emitter.
- Complex UI layout framework.
- Full `Theme` generation.
- CI that requires Godot.
- Large new game examples.
- Publishing automation.

---

# Definition Of Done For Each Milestone

A milestone is complete only when:

- relevant unit tests pass;
- generated output remains deterministic;
- snapshots are updated only intentionally;
- docs are updated when public behavior changes;
- examples still build;
- optional real Godot smoke checks pass when the task touches examples and Godot is available;
- no unrelated features are added;
- public API exports are updated if a new public helper is introduced;
- README or docs remain consistent with actual implemented behavior.
