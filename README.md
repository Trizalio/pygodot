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
| Signals | `minimal`, `timer`, `audio`, `physics`, `flappy` | supported |
| Generated GDScript | `minimal`, `pong`, `snake`, `timer`, `template_script` | raw body, source file, or template |
| InputMap | `pong`, `snake`, `flappy` | keyboard-only |
| Window settings | `pong`, `snake`, `ui_panel` | viewport size |
| External textures | `resources` | copied assets |
| External audio | `audio` | copied assets |
| External fonts | `font` | copied `.ttf` and `.tres` |
| Scene instancing | `instancing` | generated `PackedScene` references |
| Generated sub-resources | `physics`, `flappy` | basic shapes |
| `AnimationPlayer` | `animation` | minimal value tracks |
| `AudioStreamPlayer` | `audio` | basic playback wiring |
| Generated `LabelSettings` | `generated_tres`, `ui_panel` | supported |
| Generated `LabelSettings` font references | `ui_panel` | supported |
| Generated `StyleBoxFlat` | `ui_panel` | narrow UI styling |
| Build manifest ownership | `resources`, `generated_tres`, `ui_panel` | generated/copied/referenced |
| Optional real Godot smoke checks | `tools/smoke_examples.py` | optional |

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
python tools/smoke_examples.py --examples minimal,pong,snake,timer,template_script,physics,flappy
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

## Docs

- [API surface policy](docs/API_SURFACE_POLICY.md)
- [Generated/manual file boundary](docs/GENERATED_BOUNDARY.md)
- [Roadmap](docs/ROADMAP.md)
- [Next Codex roadmap](docs/NEXT_CODEX_ROADMAP.md)

Generated Godot projects are build output, not the source of truth. Edit the
Python DSL, manual assets, and referenced manual scripts, then rebuild.
