from __future__ import annotations

import os
from pathlib import Path

from pygodot import Color, ColorRect, Game, Label, Node, Node2D, Scene, Vec2, font

ROOT = Path(__file__).parent

game = Game(
    name="PygodotFont",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_window(size=Vec2(640, 360))

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
                    color=Color(0.04, 0.05, 0.08),
                ),
                Node(
                    name="Title",
                    type="Label",
                    props={
                        "text": "FontVariation resource",
                        "position": Vec2(130, 86),
                        "theme_override_fonts/font": font("res://assets/display_font.tres"),
                        "theme_override_font_sizes/font_size": 30,
                        "theme_override_colors/font_color": Color(1.0, 0.86, 0.38),
                    },
                ),
                Node(
                    name="GoogleFontTitle",
                    type="Label",
                    props={
                        "text": "Google Fonts .ttf",
                        "position": Vec2(130, 155),
                        "theme_override_fonts/font": font(
                            "res://assets/WDXL_Lubrifont_TC/WDXLLubrifontTC-Regular.ttf"
                        ),
                        "theme_override_font_sizes/font_size": 34,
                        "theme_override_colors/font_color": Color(0.58, 0.95, 1.0),
                    },
                ),
                Label(
                    "Caption",
                    text="Both font resources are copied from source_root/assets",
                    position=Vec2(130, 240),
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
