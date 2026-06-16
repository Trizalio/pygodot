from __future__ import annotations

import os
from pathlib import Path

from pygodot import Color, ColorRect, Game, Label, Node2D, Scene, Script, Vec2

ROOT = Path(__file__).parent

MAIN_SCRIPT = Script.from_file(
    source="scripts/main.gd",
    path="res://scripts/main.gd",
    extends="Node2D",
)

game = Game(
    name="PygodotMouseInput",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_window(size=Vec2(520, 320))
game.add_input_action("place_marker", mouse_buttons=["LEFT"])

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Node2D(
            "Main",
            script=MAIN_SCRIPT,
            children=[
                ColorRect(
                    "Background",
                    position=Vec2(0, 0),
                    size=Vec2(520, 320),
                    color=Color(0.05, 0.07, 0.09),
                ),
                Label(
                    "Counter",
                    text="clicks: 0",
                    position=Vec2(24, 22),
                ),
                ColorRect(
                    "Marker",
                    position=Vec2(250, 150),
                    size=Vec2(20, 20),
                    color=Color(1.0, 0.55, 0.15),
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
