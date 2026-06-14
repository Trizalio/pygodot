from __future__ import annotations

import os
from pathlib import Path

from pygodot import Color, ColorRect, Game, Label, Node2D, Scene, Vec2, label_settings

ROOT = Path(__file__).parent

game = Game(
    name="PygodotGeneratedTres",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_window(size=Vec2(640, 360))

title_settings = label_settings(
    "res://ui/title_label_settings.tres",
    font_size=36,
    font_color=Color(0.95, 1.0, 0.82),
)

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Node2D(
            "Main",
            children=[
                ColorRect(
                    "Background",
                    position=Vec2(0, 0),
                    size=Vec2(640, 360),
                    color=Color(0.04, 0.07, 0.09),
                ),
                Label(
                    "Title",
                    text="Generated LabelSettings .tres",
                    position=Vec2(96, 128),
                    label_settings=title_settings,
                ),
                Label(
                    "Caption",
                    text="The scene references a generated native Godot resource.",
                    position=Vec2(98, 190),
                    theme_override_font_sizes={"font_size": 18},
                    theme_override_colors={"font_color": Color(0.72, 0.82, 0.88)},
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
