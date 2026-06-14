# Physics Example

This example shows generated 2D collision shapes.

`game.py` creates two `Area2D` nodes with `CollisionShape2D` children. The
shapes are generated as `RectangleShape2D` sub-resources. A root script moves
the `Probe` area until Godot emits `area_entered` when it overlaps `Goal`.

Run it with:

```bash
PYTHONPATH=../../src python game.py
```
