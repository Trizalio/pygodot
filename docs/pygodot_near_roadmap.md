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
- a generated AnimationPlayer example under `examples/animation`;
- a 2D collision shape example under `examples/physics`;
- a small playable Flappy-style example under `examples/flappy`;
- generated GDScript gameplay;
- generated script bodies from source `.gd` files;
- generated script bodies from template files;
- external texture resources copied from `source_root`;
- external audio stream resources copied from `source_root`;
- external font resources copied from `source_root`;
- scene instances through `scene_instance(...)`;
- built-in Timer node signals;
- generated animation sub-resources;
- generated `RectangleShape2D` shape sub-resources;
- reusable pipe/collision gameplay with generated shape sub-resources;
- keyboard-only InputMap DSL;
- minimal window size settings;
- deterministic snapshots for example scenes/scripts;
- Godot smoke checks through `Game.check_run(...)`;
- optional multi-example smoke checks through `tools/smoke_examples.py`;
- documented generated/manual ownership boundaries.

## Next - Next Example

Pick the next example first, then add only the Godot surface that example needs.
Good candidates are direct `.tres` resource emission or another small example
that exercises a missing Godot surface.
