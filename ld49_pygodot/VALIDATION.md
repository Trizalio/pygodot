# LD49 pygodot validation

Stage G validates the generated Godot 4 project structure and documents the
manual checks that still need a human playtest.

## Automated checks

Run the normal unit suite:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

Build the LD49 project and validate the generated output:

```powershell
$env:PYTHONPATH = "src"
python -c "from ld49_pygodot.game import game; game.build()"
python tools/validate_ld49_pygodot.py
```

When `GODOT_BIN` is configured, run the optional headless smoke check:

```powershell
$env:PYTHONPATH = "src"
python -c "from ld49_pygodot.game import game; result = game.check_run(frames=20); print(result.returncode)"
```

## Manual playtest checklist

- Start the generated project in Godot 4 and confirm `main.tscn` opens first.
- Drag `Fireball`, `Frost`, `Shield`, and `Heal` onto occupied and empty tiles.
- Confirm tile highlighting clears when the cursor leaves a tile during drag.
- Click `Advance Units` and confirm units move or consume statuses.
- Confirm `Reset State` restores score, turn, tile labels, and unit cards.
- Defeat all units and confirm the end scene appears.
- Use `Open Intro`, `Preview Fader`, and the end-scene back button to check
  scene transitions.
- Inspect `.pygodot/manifest.json` and confirm generated, copied, and
  referenced ownership still match expectations.

## Known validation scope

The validator intentionally checks the current port contract, not full LD49
gameplay parity. It does not simulate drag/drop input, compare against the
original Godot 3 project, or validate final art/audio polish.
