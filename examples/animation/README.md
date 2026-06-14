# Animation Example

This example shows a generated `AnimationPlayer`.

`game.py` declares a looping value animation in Python. The `.tscn` emitter
writes the required `Animation` and `AnimationLibrary` sub-resources, then
assigns the library to the `AnimationPlayer`.

Run it with:

```bash
PYTHONPATH=../../src python game.py
```
