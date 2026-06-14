from __future__ import annotations

import os
from pathlib import Path

from pygodot import Color, ColorRect, Game, Label, Node2D, Scene, Sprite2D, Vec2, texture

ROOT = Path(__file__).parent

game = Game(
    name="PygodotResources",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/resources.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_window(size=Vec2(640, 360))

game.add_scene(
    Scene(
        path="res://scenes/resources.tscn",
        root=Node2D(
            "Resources",
            children=[
                ColorRect(
                    "Background",
                    position=Vec2(0, 0),
                    size=Vec2(640, 360),
                    color=Color(0.05, 0.06, 0.08),
                ),
                Sprite2D(
                    "Logo",
                    texture=texture("res://assets/pygodot_mark.svg"),
                    position=Vec2(320, 155),
                    scale=Vec2(2, 2),
                ),
                Label(
                    "Caption",
                    text="Texture copied from source_root/assets",
                    position=Vec2(190, 300),
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
