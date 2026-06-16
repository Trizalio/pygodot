# pygodot: LD49 Migration Roadmap for Codex

This document is the active roadmap for evolving `pygodot` toward a concrete medium-term goal: being able to rebuild and maintain an LD49-style game through `pygodot`.

It is intended to be read by Codex before making project changes. Keep work milestone-focused. Completed sprint history belongs in git commits, not in this file.

Follow the milestones in order unless the user explicitly changes direction.

---

## 1. Target Goal

The medium-term goal is to make it possible to port the LD49 game to a Godot 4 project whose project structure, scenes, resources, and build output are declared through `pygodot`.

This does **not** mean generating the original LD49 Godot 3 project byte-for-byte.

The realistic goal is:

```text
Original LD49 Godot 3 project
    -> manual Godot 4 GDScript migration where needed
    -> pygodot-generated Godot 4 project/scenes/resources
    -> runtime logic remains ordinary GDScript
```

The final LD49 port should use `pygodot` for:

- project settings;
- autoload registration;
- scene declarations;
- scene instancing;
- copied assets;
- generated or referenced resources;
- generated `.tscn`, `.gd`, `.tres`, and `project.godot` files;
- deterministic build output and tests.

Runtime gameplay logic should remain in ordinary GDScript files loaded through `Script.from_file(...)` or `Script.reference(...)`.

---

## 2. Current pygodot Baseline

`pygodot` is currently a build-time Python library for declaring Godot 4 projects and generating ordinary Godot project files.

Implemented baseline includes:

- `Game.build()`, `Game.run()`, `Game.check_run()`;
- explicit scene/node/script DSL;
- selected node constructors plus generic `node(...)`;
- typed values: `Vec2`, `Vec3`, `Rect2`, `Color`, `NodePath`;
- external resource helpers for textures, audio, fonts, generic resources, and packed scenes;
- generated scenes, scripts, `.tres` resources, and `project.godot`;
- generated `LabelSettings` resources, including font references;
- generated `StyleBoxFlat` resources;
- generated sub-resources for simple shapes and animations;
- scene instancing through generated or manual `PackedScene` resources;
- keyboard and mouse button InputMap generation;
- minimal window settings;
- explicit generated/copied/referenced resource ownership in manifest and `BuildResult`;
- optional real Godot smoke checks;
- minimal GitHub Actions unit-test CI that does not require Godot;
- examples covering small scenes, Pong, Snake, Flappy, mouse input, resources, instancing, audio, font, animation, physics, generated `.tres`, UI panel, and template scripts;
- external-project build smoke coverage and getting started documentation.

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

---

## 3. LD49 Compatibility Notes

LD49 is a Godot 3.x project. Its scenes use `format=2`, and its `project.godot` uses `config_version=4`.

`pygodot` targets Godot 4 output. Therefore, the LD49 migration must be treated as a Godot 3 -> Godot 4 migration plus a pygodot scene/project declaration rewrite.

Important LD49 features to support or consciously preserve as manual GDScript:

### Project-level requirements

LD49 uses:

- main scene registration;
- application icon;
- display window size;
- stretch mode/aspect settings;
- audio setting `output_latency.web`;
- physics setting `common/enable_pause_aware_picking`;
- many autoload singletons:
  - `SceneChanger`;
  - `Matrix`;
  - `GameState`;
  - `Animator`;
  - `Rand`;
  - `UnitsGenerator`;
  - `MatrixUtils`;
  - `Utils`;
  - `Damage`;
  - `StatusUtils`;
  - `UnitUtils`;
  - `EffectUtils`;
  - `AudioManager`.

### Scene/node requirements

LD49 scenes use many Control/UI nodes:

- `MarginContainer`;
- `Panel`;
- `VBoxContainer`;
- `HBoxContainer`;
- `GridContainer`;
- `CenterContainer`;
- `TextureRect`;
- `RichTextLabel`;
- `HSeparator`;
- `Button`;
- `Label`;
- `AudioStreamPlayer`;
- `Timer`;
- `Node2D`;
- `AnimatedSprite` in Godot 3, likely `AnimatedSprite2D` in Godot 4.

LD49 also uses:

- node groups such as `hints`;
- signal connections with `binds`;
- scene instancing through `PackedScene` resources;
- scripts with `class_name`;
- drag-and-drop Control methods:
  - `get_drag_data`;
  - `set_drag_preview`;
  - `can_drop_data`;
  - `drop_data`.

### Resource requirements

LD49 uses:

- textures;
- audio streams;
- font files;
- theme/material `.tres` files;
- shaders;
- shader materials;
- atlas textures;
- sprite frames;
- animation sub-resources;
- packed scenes;
- generated or referenced scripts.

### GDScript migration risks

LD49 scripts use Godot 3 idioms that need manual Godot 4 migration:

- `onready var` -> `@onready var`;
- `export var` -> `@export var`;
- `yield(...)` -> `await ...`;
- `.instance()` -> `.instantiate()`;
- old `connect(signal, target, method, binds)` style -> Godot 4 callable style or compatible syntax;
- old `Tween` node/interpolate API -> Godot 4 `create_tween()` style or adapted helper;
- `AnimatedSprite` -> `AnimatedSprite2D`;
- `DynamicFont`/`DynamicFontData` -> Godot 4 font resources;
- `PoolRealArray` -> Godot 4 packed arrays;
- selected property renames in Control nodes and resources.

`pygodot` should not try to automate this migration. It should make the target Godot 4 project easy to declare once the GDScript is manually updated.

---

## 4. Development Rules For Codex

Follow these rules for every task:

- Keep changes small and milestone-focused.
- Do not add unrelated features while implementing a milestone.
- Do not rewrite the public DSL unless explicitly requested.
- Preserve existing examples unless the milestone explicitly asks to change them.
- Preserve tests and snapshots unless generated output intentionally changes.
- If generated output changes, update snapshots only after verifying the change is intentional.
- Prefer explicit, boring code over clever metaprogramming.
- Do not introduce context-manager DSL or metaclass DSL.
- Do not add broad generated wrappers for the entire Godot API.
- Use `node(...)` for uncommon Godot nodes before adding convenience constructors.
- Keep public API additions documented, exported, and tested.
- Ordinary unit tests must not require a Godot binary.
- Real Godot execution must remain optional.
- Runtime gameplay logic must stay in GDScript, not Python.

---

## 5. Testing Rules

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

Do not make Godot mandatory in ordinary tests or CI.

---

# Milestone 1 - Project Autoloads And Extra Project Settings

## Goal

Add the project-level features required by LD49-style architecture.

LD49 relies heavily on autoload singletons. Without first-class autoload support, the port will either require hand-written `project.godot` or will force a rewrite of the game architecture.

## Target API

Suggested narrow API:

```python
game.add_autoload("GameState", "res://scripts/singletons/game_state.gd")
game.add_autoload("Matrix", "res://scripts/singletons/matrix.gd")
game.add_autoload("SceneChanger", "res://scripts/singletons/scene_changer.gd")
```

For project settings, either add focused helpers:

```python
game.set_icon("res://resources/characters/goblin-on-tile.png")
game.set_display(
    width=540,
    height=750,
    stretch_mode="canvas_items",
    stretch_aspect="expand",
)
```

or a narrow generic setting API:

```python
game.set_project_setting("audio/output_latency/web", 200)
game.set_project_setting("physics/common/enable_pause_aware_picking", True)
```

Prefer a minimal design that keeps project settings deterministic and testable.

## Tasks

1. Add public DSL/storage for autoload declarations.
2. Add `Game.add_autoload(...)`.
3. Normalize autoloads into IR.
4. Validate autoload names and `res://` paths.
5. Emit deterministic `[autoload]` in `project.godot`.
6. Ensure autoload script resources are copied/referenced consistently in the manifest.
7. Add minimal support for extra project settings required by LD49:
   - icon;
   - display stretch mode/aspect;
   - arbitrary setting path/value if chosen.
8. Add tests for project emitter output.
9. Update docs and README capability matrix if needed.

## Acceptance Criteria

- `project.godot` can emit `[autoload]` deterministically.
- Autoload paths can point to file-backed scripts under `res://`.
- Duplicate autoload names are rejected with clear validation errors.
- Invalid autoload paths are rejected.
- Existing project output remains stable unless intentionally updated.
- Unit tests do not require Godot.
- `python -m unittest discover -s tests` passes.

## Anti-Goals

- Do not add a full Godot `ProjectSettings` wrapper.
- Do not add a CLI.
- Do not add Godot 3 support.
- Do not require Godot in tests.
- Do not implement export presets.

## Suggested Codex Prompt

```text
Add project autoload and extra project settings support to pygodot.

Implement a narrow API:
- Game.add_autoload(name: str, path: str)
- icon/display/project setting support sufficient for LD49-style projects

ProjectEmitter must emit deterministic [autoload] and extra project settings while preserving existing [application], [input], and [display] output.

Add validation, unit tests, and project.godot snapshots.
Do not add a CLI, Godot 3 support, full ProjectSettings wrapper, or Godot-dependent tests.
python -m unittest discover -s tests must pass.
```

---

# Milestone 2 - Node Groups And Signal Binds

## Goal

Support `.tscn` features that LD49 uses directly: node groups and signal connection binds.

LD49 uses groups such as `hints`, and several button signal connections pass bound arguments like `binds=[1]` or `binds=[-1]`.

## Target API

```python
node(
    "hint",
    "Node",
    groups=["hints"],
    instance=packed_scene("res://scenes/extender.tscn"),
)
```

```python
signal(
    "pressed",
    target=".",
    method="_change_x",
    binds=[1],
)
```

## Tasks

1. Extend `Node` with `groups: list[str]`.
2. Extend `node(...)`, `scene_instance(...)`, and selected constructors to accept groups where practical.
3. Extend `SignalConnection` with `binds: list[Any]`.
4. Normalize groups and binds into IR.
5. Validate group names and serializable bind values.
6. Emit `groups=[...]` in node headers.
7. Emit `binds=[...]` in connection lines.
8. Add snapshot tests.
9. Add a tiny example or update an LD49 slice example once it exists.

## Acceptance Criteria

- Node groups are emitted deterministically.
- Signal binds are emitted deterministically.
- Existing signal behavior without binds remains unchanged.
- Unsupported bind values produce clear validation errors.
- Existing snapshots remain stable unless intentionally updated.
- `python -m unittest discover -s tests` passes.

## Anti-Goals

- Do not implement all signal connection flags unless needed.
- Do not add editor-only metadata support.
- Do not add a broad scene-file compatibility layer.
- Do not build a Godot 3 scene converter.

## Suggested Codex Prompt

```text
Add node group and signal bind support to pygodot.

Node/scene_instance should be able to emit groups=[...]. signal(...) should accept binds=[...] and TscnEmitter should emit binds in connection lines.

Keep existing signal behavior unchanged. Add validation and snapshots.
Do not implement a broad tscn compatibility layer or Godot 3 converter.
```

---

# Milestone 3 - LD49 UI Shell Support

## Goal

Make it ergonomic to describe LD49-style UI/control-heavy scenes.

LD49 heavily uses Godot Control containers and UI nodes. `pygodot` can already use generic `node(...)`, but the LD49 port will become noisy without a small set of example-backed helpers.

## Candidate Helpers

Add thin constructors only for nodes that are repeatedly used in LD49-style scenes:

- `MarginContainer`;
- `Panel`;
- `VBoxContainer`;
- `HBoxContainer`;
- `GridContainer`;
- `CenterContainer`;
- `TextureRect`;
- `RichTextLabel`;
- `HSeparator`.

These helpers should be as thin as existing node constructors.

## Example

Add:

```text
examples/ld49_ui_shell/
  README.md
  game.py
  scripts/main.gd
```

Scene should approximate the LD49 main/intro shell:

```text
Main: MarginContainer
  Panel
  VBoxContainer parts
    Label title
    TextureRect art
    CenterContainer
      VBoxContainer buttons
        Button Start
        Button Exit
  AudioStreamPlayer background
```

Use existing generated/copy resource mechanisms. Runtime script should be file-backed GDScript.

## Acceptance Criteria

- Thin UI helpers are exported from `pygodot` and `pygodot.dsl`.
- `examples/ld49_ui_shell` builds.
- Scene snapshot is deterministic.
- No layout framework is introduced.
- No full Theme generation is introduced.
- `python -m unittest discover -s tests` passes.

## Anti-Goals

- Do not wrap the full Godot UI API.
- Do not add layout abstractions.
- Do not add Theme DSL unless later examples prove it is necessary.
- Do not port the full LD49 UI yet.

## Suggested Codex Prompt

```text
Add a small LD49-style UI shell example and the minimal thin UI node constructors it needs.

Use MarginContainer, Panel, VBoxContainer, CenterContainer, TextureRect, Label, Button, and AudioStreamPlayer. Add only repeated LD49-style UI helpers, not a full Godot UI wrapper.

Add snapshots/build tests and export new helpers from pygodot.
```

---

# Milestone 4 - Autoload Scene Flow Slice

## Goal

Prove that pygodot can generate an LD49-style scene transition setup with autoload singletons.

LD49 uses `SceneChanger` and `AudioManager` singleton scripts. Main and intro scenes call those autoloads rather than owning all transition/audio logic locally.

## Example

Add:

```text
examples/ld49_scene_flow/
  README.md
  game.py
  scripts/
    scene_changer.gd
    audio_manager.gd
    main.gd
    intro.gd
    fader.gd
```

Generated scenes:

```text
main.tscn
intro.tscn
fader.tscn
```

Project should emit:

```text
[autoload]
SceneChanger="*res://scripts/scene_changer.gd"
AudioManager="*res://scripts/audio_manager.gd"
```

## Tasks

1. Use Milestone 1 autoload support.
2. Create a simple menu scene with a start button.
3. Create a second scene.
4. Add a simple fader scene or a minimal scene-change script.
5. Use copied audio if practical, otherwise keep audio manager minimal.
6. Add build tests and snapshots.
7. Add optional smoke example entry.

## Acceptance Criteria

- Generated project contains autoloads.
- Main scene can reference `SceneChanger` and `AudioManager` from GDScript.
- Multiple generated scenes are present.
- Build-only tests pass without Godot.
- Optional smoke can run when Godot is available.

## Anti-Goals

- Do not port full LD49 `SceneChanger` yet.
- Do not add complex animation/tween behavior unless needed.
- Do not require Godot in CI.

## Suggested Codex Prompt

```text
Add examples/ld49_scene_flow to prove LD49-style autoload scene transitions.

Use generated project autoloads for SceneChanger and AudioManager. Generate main, intro, and fader/minimal transition scenes. Runtime logic must remain file-backed GDScript.

Add snapshots/build tests and optional smoke runner entry.
```

---

# Milestone 5 - Animated Sprite Resource Slice

## Goal

Support the resource pattern used by LD49 unit and spell scenes.

LD49 units and spells use texture atlases, sprite frames, animated sprites, and audio players. In Godot 4, target nodes/resources should likely use `AnimatedSprite2D`, `SpriteFrames`, `AtlasTexture`, and `AudioStreamPlayer`.

## Preferred Strategy

Start with generic `sub_resource(...)` and generic `node(...)`. Add helpers only if the example becomes unreadable.

Possible DSL:

```python
frame_0 = sub_resource(
    "AtlasTexture",
    id_hint="imp_frame_0",
    atlas=texture("res://assets/small_demon.png"),
    region=Rect2(0, 0, 50, 50),
)

frames = sub_resource(
    "SpriteFrames",
    id_hint="imp_frames",
    animations=[...],
)
```

If needed later, add narrow helpers:

- `atlas_texture(...)`;
- `sprite_frames(...)`.

Do not add broad resource DSL in this milestone.

## Example

Add:

```text
examples/ld49_unit_card/
  README.md
  game.py
  scripts/unit.gd
```

Scene:

```text
Unit: Node2D
  AnimatedSprite2D
  AudioStreamPlayer spawn
  AudioStreamPlayer death
```

## Acceptance Criteria

- Generated subresources can reference external textures.
- Nested subresource-like data for `SpriteFrames` is deterministic enough for snapshots.
- Texture/audio assets are copied and recorded in manifest.
- Example approximates an LD49 unit scene.
- No full resource hierarchy is introduced.
- `python -m unittest discover -s tests` passes.

## Anti-Goals

- Do not port every LD49 unit.
- Do not implement all `SpriteFrames` options.
- Do not add Godot-assisted resource generation.
- Do not build a Godot 3 resource converter.

## Suggested Codex Prompt

```text
Add an LD49-style animated unit resource slice.

Create examples/ld49_unit_card with a Node2D unit, AnimatedSprite2D, SpriteFrames/AtlasTexture resources, and spawn/death AudioStreamPlayer nodes. Prefer generic sub_resource(...) first; add narrow helpers only if the code is unreadable.

Add snapshots, manifest assertions, and build tests.
```

---

# Milestone 6 - ShaderMaterial And Material Reference Slice

## Goal

Support LD49 spell visuals.

LD49 spell scenes use external shaders, generated or referenced `ShaderMaterial`, shader params, and external `.tres` materials.

## Tasks

1. Verify that generic `ext_resource(..., type="Shader")` is enough.
2. Add `shader(...)` helper only if it improves example readability.
3. Verify that external `.tres` material references work through generic resource helpers.
4. Generate a `ShaderMaterial` subresource using `sub_resource(...)`.
5. Ensure shader params serialize correctly.
6. Add a small spell visual example or extend `ld49_unit_card`/new `ld49_spell_card`.

## Acceptance Criteria

- Generated `ShaderMaterial` subresource can reference an external shader.
- Shader params serialize deterministically.
- External material `.tres` can be referenced and copied/referenced correctly.
- Example builds without Godot.
- `python -m unittest discover -s tests` passes.

## Anti-Goals

- Do not build a full shader DSL.
- Do not parse shader code.
- Do not generate all material resource types.
- Do not add Godot-assisted resource generation.

## Suggested Codex Prompt

```text
Add a narrow ShaderMaterial/material resource slice for LD49-style spell visuals.

Use generic ext_resource and sub_resource where possible. Add only a small shader(...) helper if it clearly improves readability. Add deterministic snapshots and manifest assertions.

Do not build a shader DSL or a full material resource system.
```

---

# Milestone 7 - LD49 Drag-And-Drop Spell Slice

## Goal

Prove the core LD49 interaction: drag a spell onto a tile.

LD49 uses Godot Control drag-and-drop methods in GDScript. `pygodot` only needs to generate the scenes and connect scripts/resources; runtime drag logic should remain in GDScript.

## Example

Add:

```text
examples/ld49_drag_spell/
  README.md
  game.py
  scripts/
    main.gd
    spell.gd
    tile.gd
```

Generated scenes:

```text
main.tscn
spell.tscn
tile.tscn
```

Scene outline:

```text
Main: MarginContainer or Control
  GridContainer map
    Tile instances
  HBoxContainer spells
    Spell instances
```

Runtime behavior:

- spell can be dragged;
- tile can accept spell drop;
- label/log counter updates when a spell is dropped;
- no full LD49 game state yet.

## Acceptance Criteria

- Tile scene is generated or referenced through `Scene.as_packed_scene()`.
- Spell scene is generated or referenced through `Scene.as_packed_scene()`.
- Drag/drop runtime logic is in file-backed GDScript.
- Groups and signal binds are available if needed.
- Build-only tests pass.
- Optional smoke can run when Godot is available.

## Anti-Goals

- Do not port all LD49 spell logic.
- Do not add Python-side drag/drop DSL.
- Do not add input abstraction for this.
- Do not port all units/statuses.

## Suggested Codex Prompt

```text
Add examples/ld49_drag_spell as a vertical slice of LD49's core interaction.

Generate Main, Spell, and Tile scenes through pygodot. Runtime drag/drop logic must remain file-backed GDScript using Godot Control methods. The slice should update a label or counter when a spell is dropped on a tile.

Do not implement full LD49 GameState, units, statuses, or spell effects.
```

---

# Milestone 8 - LD49 Godot 3 -> Godot 4 Migration Notes

## Goal

Document the manual migration work required before or during the LD49 port.

This is documentation only. Do not attempt automatic GDScript migration.

## Document

Create:

```text
docs/LD49_MIGRATION_NOTES.md
```

## Content Requirements

Include:

- the goal of the LD49 migration;
- what pygodot will generate;
- what remains manual GDScript;
- scene order for migration;
- asset/resource ownership rules;
- known Godot 3 -> 4 script changes:
  - `onready var` -> `@onready var`;
  - `export var` -> `@export var`;
  - `yield` -> `await`;
  - `.instance()` -> `.instantiate()`;
  - old signal connect syntax;
  - old Tween API;
  - `AnimatedSprite` -> `AnimatedSprite2D`;
  - `DynamicFont`/`DynamicFontData` changes;
  - `PoolRealArray` -> packed arrays;
  - selected Control property renames.
- a manual smoke checklist for the port.

## Acceptance Criteria

- Notes are specific to LD49.
- No automatic migration tooling is introduced.
- README or roadmap links to the notes.
- `python -m unittest discover -s tests` passes if docs-only changes are still checked.

## Anti-Goals

- Do not write a converter.
- Do not rewrite LD49 scripts automatically.
- Do not claim exact compatibility with Godot 3 scenes.

## Suggested Codex Prompt

```text
Add docs/LD49_MIGRATION_NOTES.md.

Document the manual Godot 3 -> Godot 4 migration issues specific to LD49 and explain which parts pygodot should generate versus which runtime GDScript remains manual.

Do not implement migration tooling.
```

---

# Milestone 9 - LD49 Vertical Slice Example

## Goal

Before porting the real LD49 repository, create a small `pygodot` example that exercises the main risks together.

## Example

Add:

```text
examples/ld49_vertical_slice/
  README.md
  game.py
  scripts/
    game_state.gd
    scene_changer.gd
    audio_manager.gd
    main.gd
    spell.gd
    tile.gd
    unit.gd
  assets/
    small placeholder textures/audio if needed
```

## Required Features

The vertical slice should include:

- autoloads;
- menu -> game scene transition;
- optional audio manager;
- 5x5 grid;
- tile scene;
- spell scene;
- drag/drop spell to tile;
- one unit scene;
- one simple animation/fade or visual feedback;
- copied assets;
- generated/referenced resources;
- manifest ownership coverage.

## Acceptance Criteria

- Builds without Godot.
- Optional smoke runs with Godot if available.
- Uses pygodot for project/scenes/resources.
- Uses GDScript for runtime logic.
- Does not introduce Python runtime or transpilation.
- Serves as the final rehearsal before the real LD49 port.

## Anti-Goals

- Do not port full LD49 content.
- Do not implement all spells/statuses/units.
- Do not make a full game.
- Do not add broad new API without example-backed need.

## Suggested Codex Prompt

```text
Add examples/ld49_vertical_slice as the final rehearsal before porting LD49.

The slice should include autoloads, menu->game scene flow, a 5x5 grid, tile and spell scenes, drag/drop spell to tile, one unit scene, simple visual feedback, copied assets, and manifest ownership assertions.

Runtime logic must stay in GDScript. Do not implement full LD49 content.
```

---

# Final Stage - Real LD49 Port

Only start this after Milestones 1-9 are complete.

The recommended port target is a new project folder or branch, not an in-place overwrite of the original Godot 3 project.

## Stage A - Skeleton Project

Create a new LD49-pygodot project structure:

```text
ld49_pygodot/
  game.py
  scripts/
  resources/
  generated/ or build/
```

Port first:

- project settings;
- autoloads;
- main scene;
- intro scene;
- fader;
- audio manager.

## Stage B - Game Scene Shell

Port the UI shell of `game.tscn`:

- root `MarginContainer`;
- score panel;
- `TextureRect` background;
- `GridContainer` map;
- spells panel;
- debug/root buttons if still useful;
- hints as referenced or generated scenes.

## Stage C - Core Runtime Scripts

Manually migrate GDScript to Godot 4:

- `GameState`;
- `Matrix`;
- `MatrixUtils`;
- `Rand`;
- `Utils`;
- `SceneChanger`;
- `AudioManager`.

## Stage D - Tile And Spell Drag/Drop

Port:

- Tile scene;
- base Spell scene;
- one spell first, preferably Fireball;
- target highlighting;
- spell drop -> cast -> next turn.

## Stage E - Units

Port:

- Unit base scene/script;
- one demon unit, e.g. Imp;
- one undead unit;
- one greenskin unit;
- movement;
- enter/exit matrix;
- one damage/status path.

## Stage F - Remaining Content

Port:

- remaining spells;
- remaining units;
- statuses;
- effects;
- end scenes;
- sounds;
- hints;
- polish.

## Stage G - Validation

Verify with:

- build-only tests;
- optional Godot smoke checks;
- manual playtest;
- gameplay comparison with original LD49.

---

# Recommended Execution Order

Use this order unless the user explicitly says otherwise:

```text
1. Project autoloads and extra project settings
2. Node groups and signal binds
3. LD49 UI shell support
4. Autoload scene flow slice
5. Animated sprite resource slice
6. ShaderMaterial/material reference slice
7. LD49 drag-and-drop spell slice
8. LD49 Godot 3 -> Godot 4 migration notes
9. LD49 vertical slice example
10. Real LD49 port
```

## Why This Order

- Autoloads unlock the LD49 architecture.
- Groups and signal binds unlock important scene-file features used by LD49.
- UI shell work validates the Control-heavy scenes.
- Scene flow validates autoload-driven transitions and audio services.
- Animated sprite and shader/material slices validate unit/spell visuals.
- Drag/drop validates the core interaction loop.
- Migration notes prevent accidental scope creep into automatic Godot 3 conversion.
- Vertical slice integrates the risky parts before touching the real LD49 content.

---

# Standing Non-Goals

Do not implement these unless the user explicitly changes direction:

- Python runtime inside Godot.
- Python-to-GDScript transpiler.
- GDExtension Python integration.
- Godot 3 `.tscn` -> pygodot converter.
- Automatic GDScript 3 -> 4 converter.
- Full Godot API wrapper generation.
- Visual editor replacement.
- ECS.
- Broad physics DSL.
- Complete resource DSL for all Godot resources.
- Godot-assisted emitter.
- Complex UI layout framework.
- Full `Theme` generation before examples prove it is needed.
- Export presets and release packaging.
- Large LD49 port before vertical slices pass.

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
- README or docs remain consistent with actual implemented behavior;
- the milestone moves the project measurably closer to the LD49 port goal.
