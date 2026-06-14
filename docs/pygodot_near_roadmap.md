# Near Roadmap

Pong and Snake are complete enough to show the current framework shape. The next
near-term work should remove pain that both examples now reveal.

## Baseline

The repository currently has:

- a minimal example under `examples/minimal`;
- a two-scene Pong example under `examples/pong`;
- a one-scene Snake example under `examples/snake`;
- a source-asset resources example under `examples/resources`;
- a generated PackedScene instancing example under `examples/instancing`;
- generated GDScript gameplay;
- generated script bodies from source `.gd` files;
- external texture resources copied from `source_root`;
- scene instances through `scene_instance(...)`;
- keyboard-only InputMap DSL;
- minimal window size settings;
- deterministic snapshots for example scenes/scripts;
- Godot smoke checks through `Game.check_run(...)`;
- documented generated/manual ownership boundaries.

## Next - Next Example

Pick the next example first, then add only the Godot surface that example needs.
Good candidates are timers, simple audio, font resources, or a tiny physics
example.
