from __future__ import annotations

import os
from pathlib import Path

from pygodot import Color, ColorRect, Game, Label, Node2D, Scene, Script, Vec2

ROOT = Path(__file__).parent

MAIN_SCRIPT = Script.from_template(
    source="scripts/main.gd.tmpl",
    path="res://scripts/main.gd",
    extends="Node2D",
    context={
        "title": "Template rendered GDScript",
        "count": 3,
    },
)

game = Game(
    name="PygodotTemplateScript",
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
            script=MAIN_SCRIPT,
            children=[
                ColorRect(
                    "Background",
                    position=Vec2(0, 0),
                    size=Vec2(640, 360),
                    color=Color(0.04, 0.05, 0.08),
                ),
                Label(
                    "StatusLabel",
                    text="waiting for template",
                    position=Vec2(150, 150),
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
