from __future__ import annotations

import os
from pathlib import Path

from pygodot import Button, Color, ColorRect, Control, Game, Label, Node2D, Scene, Script, Vec2, signal

ROOT = Path(__file__).parent

MENU_SCRIPT = Script.from_file(
    source="scripts/menu.gd",
    path="res://scripts/menu.gd",
    extends="Control",
)

PONG_SCRIPT = Script.from_file(
    source="scripts/pong.gd",
    path="res://scripts/pong.gd",
    extends="Node2D",
)

game = Game(
    name="PygodotPong",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/menu.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)

game.add_input_action("left_up", keys=["W"])
game.add_input_action("left_down", keys=["S"])
game.add_input_action("right_up", keys=["UP"])
game.add_input_action("right_down", keys=["DOWN"])
game.add_input_action("restart", keys=["SPACE"])
game.set_window(size=Vec2(800, 600))

game.add_scene(
    Scene(
        path="res://scenes/menu.tscn",
        root=Control(
            "Menu",
            script=MENU_SCRIPT,
            children=[
                ColorRect(
                    "Background",
                    position=Vec2(0, 0),
                    size=Vec2(800, 600),
                    color=Color(0.03, 0.04, 0.05),
                ),
                Label(
                    "Title",
                    text="Pygodot Pong",
                    position=Vec2(310, 160),
                ),
                Button(
                    "StartButton",
                    text="Start",
                    position=Vec2(330, 260),
                    size=Vec2(140, 44),
                    signals=[
                        signal("pressed", target=".", method="_on_start_pressed"),
                    ],
                ),
                Button(
                    "ExitButton",
                    text="Exit",
                    position=Vec2(330, 320),
                    size=Vec2(140, 44),
                    signals=[
                        signal("pressed", target=".", method="_on_exit_pressed"),
                    ],
                ),
            ],
        ),
    )
)

game.add_scene(
    Scene(
        path="res://scenes/pong.tscn",
        root=Node2D(
            "Main",
            script=PONG_SCRIPT,
            children=[
                ColorRect(
                    "Background",
                    position=Vec2(0, 0),
                    size=Vec2(800, 600),
                    color=Color(0.03, 0.04, 0.05),
                ),
                ColorRect(
                    "LeftPaddle",
                    position=Vec2(32, 252),
                    size=Vec2(18, 96),
                    color=Color(0.9, 0.95, 1.0),
                ),
                ColorRect(
                    "RightPaddle",
                    position=Vec2(750, 252),
                    size=Vec2(18, 96),
                    color=Color(1.0, 0.86, 0.45),
                ),
                ColorRect(
                    "Ball",
                    position=Vec2(392, 292),
                    size=Vec2(16, 16),
                    color=Color(1.0, 1.0, 1.0),
                ),
                Label(
                    "LeftScore",
                    text="0",
                    position=Vec2(330, 28),
                ),
                Label(
                    "RightScore",
                    text="0",
                    position=Vec2(455, 28),
                ),
                Label(
                    "HelpText",
                    text="W/S and Up/Down move paddles. Space restarts.",
                    position=Vec2(215, 560),
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
