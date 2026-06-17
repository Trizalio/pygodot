# LD49 pygodot port skeleton

This folder is the real LD49 port target scaffold. It is intentionally separate
from the old Godot 3 project and from the small `examples/ld49_*` rehearsal
slices.

Stage A covers only the skeleton:

- project settings;
- autoload declarations;
- main scene;
- intro scene;
- fader scene;
- copied placeholder icon resource;
- source-owned autoload scripts, including `AudioManager`.

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
