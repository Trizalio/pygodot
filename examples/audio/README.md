# Audio Resource Example

This example shows a source-owned audio file copied into the generated Godot
project.

`game.py` declares an `AudioStreamPlayer` whose `stream` points at
`res://assets/tone.wav`. During `game.build()`, pygodot copies the WAV from
`examples/audio/assets` into `build/godot_project/assets`, emits it as an
external `AudioStream` resource, and records it in the manifest.

Run it with:

```bash
PYTHONPATH=../../src python game.py
```
