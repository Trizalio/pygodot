# Snake Example

This example builds a single-scene Snake project from the pygodot Python DSL.
The scene stays minimal and renders the game board from generated GDScript with
`_draw()`.

From the repository root:

```powershell
$env:PYTHONPATH = "src"
python examples/snake/game.py
```

To build without launching Godot:

```powershell
$env:PYTHONPATH = "src"
python -c "from examples.snake.game import game; game.build()"
```

To run a short headless smoke check:

```powershell
$env:PYTHONPATH = "src"
python -c "from examples.snake.game import game; game.check_run(frames=20)"
```

Controls:

- Move: `W/A/S/D` or arrow keys
- Restart: `Space`
