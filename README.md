# pygodot

`pygodot` is a build-time Python library for declaring Godot 4 projects and
generating normal Godot files.

Python is used to describe scenes, resources, scripts, and project structure.
Runtime logic remains ordinary GDScript inside the generated Godot project.

## What It Is

- A library-first Python API centered on `Game`, `Scene`, nodes, scripts, and
  resources.
- A direct emitter for native Godot project files: `.tscn`, `.gd`, `.tres`, and
  `project.godot`.
- A source-driven workflow where generated Godot projects are build output.
- A small, example-backed DSL rather than a broad wrapper for all of Godot.

## What It Is Not

- Not a Python runtime inside Godot.
- Not a Python-to-GDScript transpiler.
- Not a replacement for the Godot editor.
- Not a generated wrapper for the full Godot API.
- Not a JSON/YAML intermediate representation pipeline.

## Capability Matrix

| Feature | Example | Status |
| --- | --- | --- |
| Scene generation | `minimal` | supported |
| Project autoloads | LD49 roadmap slices | generated `[autoload]` |
| Project settings | LD49 roadmap slices | icon, display stretch, focused extra settings |
| Signals | `minimal`, `timer`, `audio`, `physics`, `flappy` | supported |
| Signal binds and node groups | `ld49_ui_shell` | supported |
| Generated GDScript | `minimal`, `pong`, `snake`, `timer`, `template_script` | raw body, source file, or template |
| InputMap | `pong`, `snake`, `flappy`, `mouse_input` | keyboard and mouse buttons |
| Window settings | `pong`, `snake`, `ui_panel` | viewport size |
| External textures | `resources` | copied assets |
| External audio | `audio` | copied assets |
| External fonts | `font` | copied `.ttf` and `.tres` |
| Scene instancing | `instancing` | generated `PackedScene` references |
| Generated sub-resources | `physics`, `flappy` | basic shapes |
| Animated sprite resources | `ld49_unit_card` | generic `AtlasTexture` and `SpriteFrames` |
| `AnimationPlayer` | `animation` | minimal value tracks |
| `AudioStreamPlayer` | `audio` | basic playback wiring |
| Generated `LabelSettings` | `generated_tres`, `ui_panel` | supported |
| Generated `LabelSettings` font references | `ui_panel` | supported |
| Generated `StyleBoxFlat` | `ui_panel` | narrow UI styling |
| Control/UI containers | `ld49_ui_shell` | narrow LD49-style helpers |
| Autoload scene flow | `ld49_scene_flow` | SceneChanger/AudioManager slice |
| LD49 vertical slice | `ld49_vertical_slice` | final rehearsal example |
| Build manifest ownership | `resources`, `generated_tres`, `ui_panel` | generated/copied/referenced |
| Optional real Godot smoke checks | `tools/smoke_examples.py` | optional |

## Install From Checkout

`pygodot` is an early `0.1.x` technical package. Install it from a local
checkout while developing or trying it from another project:

```powershell
python -m pip install -e C:\path\to\pygodot
```

Then create a separate project directory:

```powershell
mkdir my_game
cd my_game
```

Create a `game.py` that imports `pygodot`, constructs a `Game` with
`source_root=Path(__file__).parent`, and calls `game.build()`. The generated
Godot project can live under a local build directory such as `build/godot`.
Godot is only needed when calling `game.run()` or `game.check_run()`.

For a complete external-project walkthrough, see
[Getting started](docs/GETTING_STARTED.md).

For the LD49 Godot 3 to Godot 4 port plan, see
[LD49 migration notes](docs/LD49_MIGRATION_NOTES.md).

The real LD49 port scaffold starts in [ld49_pygodot](ld49_pygodot/README.md).

## Examples

| Example | Description |
| --- | --- |
| `examples/minimal` | One generated scene with a label, button, signal, and inline script. |
| `examples/pong` | Playable two-scene Pong with keyboard input and file-backed scripts. |
| `examples/snake` | Draw-based Snake using keyboard InputMap actions. |
| `examples/resources` | Copies a source-owned SVG texture into the generated project. |
| `examples/instancing` | Reuses a generated scene through `Scene.as_packed_scene()`. |
| `examples/timer` | Connects a `Timer.timeout` signal to generated GDScript. |
| `examples/template_script` | Renders generated GDScript from a `string.Template` file. |
| `examples/audio` | Copies and plays a source-owned WAV with `AudioStreamPlayer`. |
| `examples/font` | Uses copied `.ttf` and `.tres` font resources on labels. |
| `examples/animation` | Generates `AnimationPlayer` value tracks and animation sub-resources. |
| `examples/physics` | Uses `Area2D`, `CollisionShape2D`, and generated rectangle shapes. |
| `examples/flappy` | Small playable flappy-style example with input, timers, and collisions. |
| `examples/generated_tres` | Generates a `LabelSettings` `.tres` resource. |
| `examples/ui_panel` | Static dashboard using generated typography and panel style resources. |
| `examples/mouse_input` | Moves a marker and increments a counter on left click. |
| `examples/ld49_ui_shell` | LD49-style menu shell with Control containers and copied art. |
| `examples/ld49_scene_flow` | LD49-style autoload scene transition slice. |
| `examples/ld49_unit_card` | LD49-style animated unit scene with copied texture/audio assets. |
| `examples/ld49_spell_card` | LD49-style shader material spell visual slice. |
| `examples/ld49_drag_spell` | LD49-style drag-and-drop spell onto tile interaction slice. |
| `examples/ld49_vertical_slice` | LD49-style final rehearsal with autoloads, grid, drag/drop, unit, and resources. |

## Run

Set `PYTHONPATH` while working from the repository:

```powershell
$env:PYTHONPATH = "src"
```

Run an example:

```powershell
python examples/pong/game.py
```

Set `GODOT_BIN` if your Godot executable is not available as `godot`:

```powershell
$env:GODOT_BIN = "C:\Path\To\Godot.exe"
```

Build without launching Godot:

```powershell
python -c "from examples.pong.game import game; game.build()"
```

Run a short headless smoke check:

```powershell
python -c "from examples.pong.game import game; game.check_run(frames=20)"
```

Run optional smoke checks for multiple examples:

```powershell
python tools/smoke_examples.py --examples minimal,pong,snake,timer,template_script,physics,flappy,mouse_input
python tools/smoke_examples.py --all --frames 20
```

If Godot is not available, the smoke runner skips by default. Use
`--require-godot` when missing Godot should fail the command.

## Test

Ordinary unit tests do not require Godot:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

CI runs the same unit test suite without installing or launching Godot.

## Docs

- [Getting started](docs/GETTING_STARTED.md)
- [API surface policy](docs/API_SURFACE_POLICY.md)
- [Generated/manual file boundary](docs/GENERATED_BOUNDARY.md)
- [Build manifest](docs/MANIFEST.md)
- [Roadmap](docs/ROADMAP.md)
- [Next Codex roadmap](docs/NEXT_CODEX_ROADMAP.md)

The API surface policy marks which public helpers are stable for the 0.1 line
and which remain experimental while the examples continue to shape them.

Generated Godot projects are build output, not the source of truth. Edit the
Python DSL, manual assets, and referenced manual scripts, then rebuild.
