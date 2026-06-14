from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    AnimationPlayer,
    Color,
    ColorRect,
    Game,
    Label,
    Node2D,
    Scene,
    Vec2,
    animation,
    key,
    value_track,
)

ROOT = Path(__file__).parent

PULSE_ANIMATION = animation(
    "pulse",
    length=1.2,
    loop=True,
    tracks=[
        value_track(
            "Pulse:scale",
            keys=[
                key(0.0, Vec2(1.0, 1.0)),
                key(0.6, Vec2(1.35, 1.35)),
                key(1.2, Vec2(1.0, 1.0)),
            ],
        ),
        value_track(
            "Pulse:color",
            keys=[
                key(0.0, Color(0.2, 0.85, 1.0)),
                key(0.6, Color(1.0, 0.66, 0.25)),
                key(1.2, Color(0.2, 0.85, 1.0)),
            ],
        ),
    ],
)

game = Game(
    name="PygodotAnimation",
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
                Label(
                    "Title",
                    text="AnimationPlayer generated from Python",
                    position=Vec2(160, 70),
                ),
                ColorRect(
                    "Pulse",
                    position=Vec2(295, 160),
                    size=Vec2(50, 50),
                    scale=Vec2(1.0, 1.0),
                    color=Color(0.2, 0.85, 1.0),
                ),
                AnimationPlayer(
                    "Animator",
                    autoplay="pulse",
                    animations=[PULSE_ANIMATION],
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
