from __future__ import annotations

import os
from pathlib import Path

from pygodot import Game, Node2D, Scene, Script, Vec2

ROOT = Path(__file__).parent

SNAKE_SCRIPT = Script.from_file(
    source="scripts/snake.gd",
    path="res://scripts/snake.gd",
    extends="Node2D",
)

game = Game(
    name="PygodotSnake",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/snake.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)

game.add_input_action("move_up", keys=["W", "UP"])
game.add_input_action("move_down", keys=["S", "DOWN"])
game.add_input_action("move_left", keys=["A", "LEFT"])
game.add_input_action("move_right", keys=["D", "RIGHT"])
game.add_input_action("restart", keys=["SPACE"])
game.set_window(size=Vec2(672, 560))

game.add_scene(
    Scene(
        path="res://scenes/snake.tscn",
        root=Node2D("Snake", script=SNAKE_SCRIPT),
    )
)

if __name__ == "__main__":
    game.run()
