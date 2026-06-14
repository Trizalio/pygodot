# pygodot

`pygodot` is a build-time Python library for declaring Godot 4 projects and
generating normal Godot files.

Python is used to describe scenes and project structure. Runtime logic remains
ordinary GDScript inside the generated Godot project.

## Current Examples

Minimal example:

```powershell
$env:PYTHONPATH = "src"
python examples/minimal/game.py
```

Playable Pong example:

```powershell
$env:PYTHONPATH = "src"
python examples/pong/game.py
```

Draw-based Snake example:

```powershell
$env:PYTHONPATH = "src"
python examples/snake/game.py
```

Set `GODOT_BIN` if your Godot executable is not available as `godot`:

```powershell
$env:GODOT_BIN = "C:\Path\To\Godot.exe"
```

To build without launching Godot:

```powershell
$env:PYTHONPATH = "src"
python -c "from examples.pong.game import game; game.build()"
```

To run a short headless Godot smoke check:

```powershell
$env:PYTHONPATH = "src"
python -c "from examples.pong.game import game; game.check_run(frames=20)"
```

To run optional smoke checks for multiple examples:

```powershell
$env:PYTHONPATH = "src"
python tools/smoke_examples.py --examples minimal,pong,snake,timer,physics,flappy
python tools/smoke_examples.py --all --frames 20
```

If Godot is not available, the smoke runner skips by default. Use
`--require-godot` when missing Godot should fail the command.

Generated Godot projects are build output, not the source of truth. See
`docs/GENERATED_BOUNDARY.md` for the generated/manual file ownership policy.

## Run Tests

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```
