# Minimal Example

This example declares a tiny Godot project with one scene, a label, a button,
and a raw GDScript signal handler.

From the repository root:

```powershell
$env:PYTHONPATH = "C:\code\PyGodot\src"
$env:GODOT_BIN = "C:\godot\Godot_v4.6.3\Godot_v4.6.3-stable_win64.exe"
C:\code\PyGodot\.venv\Scripts\python.exe C:\code\PyGodot\examples\minimal\game.py
```

To build without running Godot:

```powershell
$env:PYTHONPATH = "C:\code\PyGodot\src"
C:\code\PyGodot\.venv\Scripts\python.exe -c "from examples.minimal.game import game; game.build()"
```
