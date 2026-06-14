# Flappy Example

This example is a small Flappy Bird style game built from generated Godot
scenes and source-backed GDScript.

It uses only generated rectangles:

- `Area2D` collision zones;
- `CollisionShape2D` nodes backed by generated `RectangleShape2D`
  sub-resources;
- `Timer.timeout` and `Area2D.area_entered` signals;
- keyboard input actions for flap and restart.

Run it with:

```bash
PYTHONPATH=../../src python game.py
```
