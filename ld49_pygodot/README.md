# LD49 pygodot port skeleton

This folder is the real LD49 port target scaffold. It is intentionally separate
from the old Godot 3 project and from the small `examples/ld49_*` rehearsal
slices.

Implemented so far:

- project settings;
- autoload declarations;
- main scene;
- intro scene;
- fader scene;
- copied placeholder icon resource;
- source-owned autoload scripts, including `AudioManager`.
- Stage B `main.tscn` shell with a score panel, `TextureRect` background, 5x5
  map grid, spells panel, debug buttons, and a generated hint scene instance.
- Stage C core runtime singletons: `GameState`, `Matrix`, `MatrixUtils`,
  `Rand`, `Utils`, `SceneChanger`, and `AudioManager`.
- Stage D reusable tile and spell scenes with drag/drop spell targeting,
  runtime tile signal wiring, and a simple `GameState.apply_spell(...)` turn
  update path.
- Stage E unit scene/card wiring with Imp, Bones, and Gob units, simple
  matrix-backed movement, and a Fireball damage/status path.

Runtime behavior remains ordinary GDScript. This folder does not contain an
automatic Godot 3 to Godot 4 converter and does not claim to be a full LD49
port yet.

Build it from the repository root with:

```powershell
$env:PYTHONPATH = "src"
python -c "from ld49_pygodot.game import game; game.build()"
```

Run a short Godot smoke check when `GODOT_BIN` is configured:

```powershell
$env:PYTHONPATH = "src"
python -c "from ld49_pygodot.game import game; result = game.check_run(frames=20); print(result.returncode)"
```
