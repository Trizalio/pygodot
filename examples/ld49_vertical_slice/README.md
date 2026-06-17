# LD49 vertical slice example

This example is the final pygodot rehearsal before attempting a real LD49 port.
It deliberately combines the main risks from the earlier LD49 slices:

- autoload singletons for game state, scene changes, and audio cues;
- menu to battle scene transition;
- 5x5 tile grid generated through reusable `tile.tscn` instances;
- draggable spell cards generated through reusable `spell.tscn` instances;
- one reusable unit scene with a copied SVG portrait asset;
- drag/drop runtime behavior in file-backed GDScript;
- tile/unit visual feedback through Godot 4 tweens;
- generated `StyleBoxFlat` resource ownership in the manifest.

The example is intentionally not a full game. It proves that pygodot can emit
the project/scenes/resources while LD49 runtime behavior stays in ordinary
GDScript.
