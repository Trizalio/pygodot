# pygodot
Declarative python framework to create godot projects

## Run the example from a source checkout

```powershell
$env:PYTHONPATH = "C:\code\PyGodot\src"
C:\code\PyGodot\.venv\Scripts\python.exe C:\code\PyGodot\example.py
```

The example owns a `Game` object and calls `game.run()`, which builds the Godot
project, runs Godot import, and starts the generated main scene.

## Run tests

```powershell
$env:PYTHONPATH = "C:\code\PyGodot\src"
C:\code\PyGodot\.venv\Scripts\python.exe -m unittest discover -s tests
```
