# LD49 scene flow example

This example proves the LD49-style scene flow shape: generated scenes call
autoload singletons for scene transitions and audio state.

Runtime behavior is ordinary file-backed GDScript. `pygodot` only declares the
project, autoload registration, scenes, signal wiring, and generated output.
