from __future__ import annotations

import os
from pathlib import Path

from pygodot import Color, ColorRect, Game, Label, Node2D, Scene, Vec2, packed_scene, scene_instance

ROOT = Path(__file__).parent

game = Game(
    name="PygodotInstancing",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_window(size=Vec2(640, 360))

game.add_scene(
    Scene(
        path="res://scenes/gem.tscn",
        root=Node2D(
            "Gem",
            children=[
                ColorRect(
                    "Shadow",
                    position=Vec2(-22, 16),
                    size=Vec2(44, 10),
                    color=Color(0, 0, 0, 0.28),
                ),
                ColorRect(
                    "Body",
                    position=Vec2(-18, -18),
                    size=Vec2(36, 36),
                    color=Color(0.2, 0.85, 1.0),
                ),
                ColorRect(
                    "Highlight",
                    position=Vec2(-10, -14),
                    size=Vec2(14, 10),
                    color=Color(0.85, 1.0, 1.0),
                ),
            ],
        ),
    )
)

gem_scene = packed_scene("res://scenes/gem.tscn")

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
                Label(
                    "Title",
                    text="Three instances, one generated scene",
                    position=Vec2(180, 48),
                ),
                scene_instance("GemA", gem_scene, position=Vec2(220, 190)),
                scene_instance("GemB", gem_scene, position=Vec2(320, 150), scale=Vec2(1.35, 1.35)),
                scene_instance("GemC", gem_scene, position=Vec2(430, 205)),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
