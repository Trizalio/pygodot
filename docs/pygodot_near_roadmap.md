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
- a signal-connected timer example under `examples/timer`;
- an audio resource example under `examples/audio`;
- a font resource example under `examples/font`;
- generated GDScript gameplay;
- generated script bodies from source `.gd` files;
- external texture resources copied from `source_root`;
- external audio stream resources copied from `source_root`;
- external font resources copied from `source_root`;
- scene instances through `scene_instance(...)`;
- built-in Timer node signals;
- keyboard-only InputMap DSL;
- minimal window size settings;
- deterministic snapshots for example scenes/scripts;
- Godot smoke checks through `Game.check_run(...)`;
- documented generated/manual ownership boundaries.

## Next - Next Example

Pick the next example first, then add only the Godot surface that example needs.
Good candidates are animation, a tiny physics example, or direct `.tres`
resource emission.
