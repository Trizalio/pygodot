# LD49 drag spell example

This example is a vertical slice of the core LD49 interaction: drag a spell
card onto a map tile.

`pygodot` generates the main scene plus reusable `spell.tscn` and `tile.tscn`
scenes. Runtime drag-and-drop logic stays in ordinary file-backed GDScript using
Godot `Control` methods: `_get_drag_data`, `_can_drop_data`, and `_drop_data`.

Dropping a spell updates the tile state and emits a signal back to the main
scene, which updates the log label.
