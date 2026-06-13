# Minimal Example

This example declares a tiny Godot project with one scene, a label, a button,
and a generated GDScript signal handler.

From the repository root:

```powershell
$env:PYTHONPATH = "src"
python examples/minimal/game.py
```

To build without launching Godot:

```powershell
$env:PYTHONPATH = "src"
python -c "from examples.minimal.game import game; game.build()"
```

Set `GODOT_BIN` if your Godot executable is not available as `godot`.
