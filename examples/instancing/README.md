# Scene Instancing Example

This example shows one generated scene reused as a `PackedScene` instance.

`res://scenes/gem.tscn` is generated from Python DSL. `res://scenes/main.tscn`
references it with `packed_scene(...)` and creates three `scene_instance(...)`
nodes with different transforms.

Run it with:

```bash
PYTHONPATH=../../src python game.py
```
