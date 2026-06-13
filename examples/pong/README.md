# Pong example

This example builds a two-scene Pong project from the pygodot Python DSL.
Python is used only at build time; the generated Godot project runs ordinary
GDScript.

## Build

From the repository root:

```powershell
python examples/pong/game.py
```

The script calls `game.run()`, which builds the Godot project and then starts it
with the configured Godot binary.

To only build the project from Python:

```powershell
python -c "from examples.pong.game import game; game.build()"
```

To run a short headless smoke check that exits automatically and reports Godot
script errors:

```powershell
python -c "from examples.pong.game import game; game.check_run(frames=20)"
```

Generated files are written under:

```text
examples/pong/build/godot_project/
```

## Run

By default pygodot uses `godot`. Set `GODOT_BIN` if your Godot executable has a
different name or path:

```powershell
$env:GODOT_BIN = "C:\Path\To\Godot.exe"
python examples/pong/game.py
```

Controls:

- Menu: click `Start` to play or `Exit` to quit
- Left paddle: `W` / `S`
- Right paddle: `Up` / `Down`
- Restart: `Space`

The controls are declared with pygodot input actions in `game.py` and emitted to
the generated `project.godot` InputMap.
