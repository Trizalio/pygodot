# LD49 Migration Notes

These notes describe the manual Godot 3 to Godot 4 work expected during the
LD49 port. They are planning notes, not migration tooling.

`pygodot` should generate ordinary Godot 4 project files for the port while
runtime behavior remains ordinary GDScript. The generated project must stay
openable, debuggable, and runnable in Godot 4.

## Migration Goal

The LD49 migration goal is to rebuild the game as a native Godot 4 project with
explicit generated ownership boundaries:

- declare scenes, project settings, reusable generated resources, and selected
  resource references in Python;
- emit Godot 4 `.tscn`, `.gd`, `.tres`, and `project.godot` files;
- keep gameplay logic, drag/drop behavior, spell resolution, and stateful
  runtime behavior in reviewed GDScript;
- preserve LD49's tactical loop in small vertical slices before attempting a
  full port.

The current pygodot examples map to intended LD49 slices:

- `examples/ld49_ui_shell` for Control/container layout and signals;
- `examples/ld49_scene_flow` for autoload scene changes and audio cues;
- `examples/ld49_unit_card` for animated unit visuals and copied assets;
- `examples/ld49_spell_card` for shader/material spell visuals;
- `examples/ld49_drag_spell` for dragging a spell onto a tile.
- `examples/ld49_vertical_slice` for the final combined rehearsal before the
  real LD49 port.
- `ld49_pygodot/` for the real port target, starting with the Stage A skeleton
  project.

## What Pygodot Should Generate

Use pygodot for deterministic build-time structure:

- `project.godot` application metadata, display settings, focused project
  settings, InputMap actions, and autoload declarations;
- generated LD49 shell scenes such as intro/menu/main/fader scenes;
- generated reusable tile, spell, and unit scene skeletons;
- generated scene instances through `Scene.as_packed_scene()` and
  `scene_instance(...)`;
- explicit signal connections and optional bind arguments where the connection
  shape is static;
- generated GDScript wrapper files from source-backed `.gd` files where pygodot
  owns the destination path;
- narrow generated `.tres` resources such as `LabelSettings`, `StyleBoxFlat`,
  and simple `ShaderMaterial` resources;
- scene-local sub-resources such as collision shapes, `AtlasTexture`,
  `SpriteFrames`, and small shader material resources;
- copied source-owned assets when they are referenced explicitly from Python.

Generated files should remain under pygodot-owned paths and should be treated as
build output. Do not silently overwrite manually edited Godot project files.

## What Remains Manual GDScript

Keep LD49 runtime behavior in manual GDScript files:

- tactical game state and turn progression;
- unit health, status effects, target selection, and spell resolution;
- Control drag-and-drop methods such as `_get_drag_data`, `_can_drop_data`, and
  `_drop_data`;
- animation playback decisions and timing-sensitive scene behavior;
- save/load behavior;
- random number use and deterministic game rules;
- audio cue policy beyond static player/resource wiring;
- UI copy, balance data, and tuning tables when they are easier to review as
  Godot-facing source files.

Do not introduce Python-in-Godot runtime support, a Python-to-GDScript
transpiler, or an automatic Godot 3 script converter for this migration.

## Suggested Scene Order

Migrate in small, runnable slices:

1. Project shell: `project.godot`, display settings, input actions, and
   autoload declarations.
2. Menu and intro scenes: static Control layout, buttons, and scene transition
   smoke checks.
3. Fader/scene changer: verify autoload scene flow before gameplay scenes.
4. Audio manager: copy or reference cues, then verify visible logging for cue
   playback state.
5. Unit scene: animated sprite resources, unit labels, click or selection
   behavior.
6. Spell visual scene: shader/material references and generated
   `ShaderMaterial` parameters.
7. Tile scene: reusable tile visuals, groups, and drop targets.
8. Main battle board: instantiate tiles, units, and spell cards through
   `PackedScene` references.
9. Drag/drop interaction: drag a spell to a tile and update a visible log or
   counter.
10. Tactical rules: manually port spell effects and turn resolution after the
    scene/resource structure is stable.

Each step should build without Godot and preferably run through a short Godot
smoke check when `GODOT_BIN` is available.

## Asset And Resource Ownership

Use explicit ownership rules during the port:

- Python-declared generated files are pygodot-owned build output.
- Source-owned assets live under the example or LD49 source tree and are copied
  when referenced by helpers such as `texture(...)`, `audio_stream(...)`,
  `font(...)`, `shader(...)`, `packed_scene(...)`, or `ext_resource(...)`.
- Source-owned `.tres` files are copied as files. Pygodot does not parse copied
  `.tres` files to discover nested dependencies.
- If a copied `.tres` depends on a shader, texture, or font, declare that
  dependency explicitly somewhere pygodot can see it when it must be copied or
  tracked.
- Generated `.tres` resources may declare their own explicit external
  dependencies, such as `LabelSettings.font` or `ShaderMaterial.shader`.
- Missing external resources remain soft references and should be visible in
  the build manifest as `ownership="referenced"`.
- The `.pygodot/manifest.json` file is the first place to check whether a
  resource was generated, copied, or only referenced.

## Godot 3 To Godot 4 Script Changes

Review LD49 scripts manually for these common changes.

### Variables And Await

- `onready var node = $Path` becomes `@onready var node = $Path`.
- `export var value = 1` becomes `@export var value = 1`.
- `yield(signal_owner, "signal_name")` becomes `await signal_owner.signal_name`.
- `yield(get_tree().create_timer(0.5), "timeout")` becomes
  `await get_tree().create_timer(0.5).timeout`.

### Instances And Signals

- `PackedScene.instance()` becomes `PackedScene.instantiate()`.
- Old connect syntax such as
  `button.connect("pressed", self, "_on_pressed")` should become callable-based
  Godot 4 syntax, for example `button.pressed.connect(_on_pressed)`.
- When arguments were passed through old signal binds, verify the callable or
  generated `[connection ... binds=[...]]` output explicitly.
- Signal declarations should use Godot 4 typed syntax when practical:
  `signal spell_dropped(tile_id: String, spell_id: String)`.

### Tween And Animation

- Godot 3 `Tween` node workflows should be reviewed. Godot 4 commonly uses
  `create_tween()` and chained tween calls.
- Check old `interpolate_property`, `start`, and callback usage. These usually
  need hand migration, especially for faders and spell effects.
- `AnimatedSprite` becomes `AnimatedSprite2D`.
- `AnimatedSprite.frames` and animation names should be checked against
  generated `SpriteFrames` resources.
- AnimationPlayer tracks should be validated in Godot after emission, especially
  paths that changed due to scene restructuring.

### Fonts And UI

- `DynamicFont` and `DynamicFontData` were replaced by Godot 4 font resources
  and label settings workflows. Prefer copied `.ttf` files and generated or
  source-owned `LabelSettings` resources.
- Several Control layout properties changed or became more explicit. Audit
  anchors, offsets, size flags, `custom_minimum_size`, alignment fields, and
  theme override paths.
- `rect_position`, `rect_size`, and related Godot 3 Control property names may
  need Godot 4 equivalents such as `position`, `size`, or offset/anchor
  settings depending on the node.
- `align` and `valign` on labels should be checked against
  `horizontal_alignment` and `vertical_alignment`.

### Arrays And Types

- `PoolRealArray` becomes `PackedFloat32Array`.
- Other Godot 3 pool arrays map to Godot 4 packed arrays, such as
  `PackedVector2Array`, `PackedStringArray`, and `PackedColorArray`.
- Add type hints gradually where they clarify signal payloads and drag/drop
  dictionaries, but avoid broad rewrites that change behavior.

### Gameplay-Specific Checks

- Drag/drop spell data should be a small dictionary or typed Resource-like
  payload that tiles can validate.
- Tile IDs, unit IDs, and spell IDs should be stable strings that can be passed
  through signals and logged during smoke checks.
- Any old global singleton paths should be verified against generated autoload
  names in `project.godot`.
- Pause, input picking, and mouse handling should be tested in Godot because
  Control and Area2D input order can shift during migration.

## Manual Smoke Checklist

Run this checklist after each LD49 migration slice:

- Build the pygodot project from Python without launching Godot.
- Open the generated project in Godot 4 and verify there are no import errors.
- Run the generated main scene for at least a short smoke pass.
- Confirm `project.godot` has the expected main scene, display settings,
  InputMap actions, and autoload names.
- Inspect `.pygodot/manifest.json` for generated/copied/referenced ownership.
- Verify every generated scene opens in the Godot editor.
- Click menu buttons and confirm signal-connected labels/logs update.
- Trigger scene changes through the autoload scene changer.
- Play one audio cue and confirm the visible/logged state changes.
- Instantiate at least one unit, spell, and tile scene in the battle scene.
- Drag one spell onto one tile and confirm the tile and log update.
- Trigger one unit animation and one spell material visual.
- Check exported variables overridden on scene instances, such as tile IDs and
  spell IDs.
- Review Godot output for warnings that point to renamed properties or invalid
  node paths.
- Keep any manual fixes in source-owned scripts/resources, not generated build
  output.

## Non-Goals

- No automatic Godot 3 to Godot 4 converter.
- No automatic GDScript rewrite.
- No claim that Godot 3 `.tscn` scenes can be consumed directly.
- No broad generated wrapper for every Godot node, resource, or property.
