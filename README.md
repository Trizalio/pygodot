# pygodot
Declarative python framework to create godot projects

## Run the example from a source checkout

```powershell
$env:PYTHONPATH = "C:\code\PyGodot\src"
C:\code\PyGodot\.venv\Scripts\python.exe C:\code\PyGodot\example.py
```

The example owns a `Game` object and calls `game.run()`, which builds the Godot
project, runs Godot import, and starts the generated main scene.

There is also a self-contained minimal example at `examples/minimal/game.py`.

Generated Godot projects are build output, not the source of truth. See
`docs/GENERATED_BOUNDARY.md` for the generated/manual file ownership policy.

## Run tests

```powershell
$env:PYTHONPATH = "C:\code\PyGodot\src"
C:\code\PyGodot\.venv\Scripts\python.exe -m unittest discover -s tests
```
