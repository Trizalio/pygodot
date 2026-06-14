# Resources Example

This example shows a source-owned asset copied into the generated Godot project.

`game.py` declares a `Sprite2D` whose `texture` points at
`res://assets/pygodot_mark.svg`. During `game.build()`, pygodot copies the SVG
from `examples/resources/assets` into `build/godot_project/assets`, emits it as
an external `Texture2D` resource in the scene, and records it in the manifest.

Run it with:

```bash
PYTHONPATH=../../src python game.py
```
