from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    Area2D,
    CollisionShape2D,
    Color,
    ColorRect,
    Game,
    Label,
    Node2D,
    Scene,
    Script,
    Timer,
    Vec2,
    rectangle_shape_2d,
    signal,
)

ROOT = Path(__file__).parent

MAIN_SCRIPT = Script.from_file(
    source="scripts/main.gd",
    path="res://scripts/main.gd",
    extends="Node2D",
)

BIRD_SHAPE = rectangle_shape_2d(size=Vec2(34, 26))
GROUND_SHAPE = rectangle_shape_2d(size=Vec2(480, 80))
PIPE_SHAPE = rectangle_shape_2d(size=Vec2(60, 480))


def solid_area(
    name: str,
    *,
    position: Vec2,
    visual_size: Vec2,
    visual_color: Color,
    shape,
    shape_name: str,
):
    return Area2D(
        name,
        position=position,
        children=[
            ColorRect(
                f"{name}Visual",
                position=Vec2(-visual_size.x / 2, -visual_size.y / 2),
                size=visual_size,
                color=visual_color,
            ),
            CollisionShape2D(shape_name, shape=shape),
        ],
    )


game = Game(
    name="PygodotFlappy",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_window(size=Vec2(480, 720))
game.add_input_action("flap", keys=["SPACE", "UP"])
game.add_input_action("restart", keys=["R"])

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
                    size=Vec2(480, 720),
                    color=Color(0.08, 0.12, 0.18),
                ),
                Area2D(
                    "Bird",
                    position=Vec2(140, 310),
                    signals=[
                        signal("area_entered", target=".", method="_on_bird_area_entered"),
                    ],
                    children=[
                        ColorRect(
                            "BirdVisual",
                            position=Vec2(-17, -13),
                            size=Vec2(34, 26),
                            color=Color(1.0, 0.82, 0.24),
                        ),
                        CollisionShape2D("BirdShape", shape=BIRD_SHAPE),
                    ],
                ),
                solid_area(
                    "Ground",
                    position=Vec2(240, 680),
                    visual_size=Vec2(480, 80),
                    visual_color=Color(0.32, 0.48, 0.26),
                    shape=GROUND_SHAPE,
                    shape_name="GroundShape",
                ),
                solid_area(
                    "PipeTopA",
                    position=Vec2(560, 60),
                    visual_size=Vec2(60, 480),
                    visual_color=Color(0.16, 0.74, 0.36),
                    shape=PIPE_SHAPE,
                    shape_name="PipeTopAShape",
                ),
                solid_area(
                    "PipeBottomA",
                    position=Vec2(560, 560),
                    visual_size=Vec2(60, 480),
                    visual_color=Color(0.16, 0.74, 0.36),
                    shape=PIPE_SHAPE,
                    shape_name="PipeBottomAShape",
                ),
                solid_area(
                    "PipeTopB",
                    position=Vec2(850, 120),
                    visual_size=Vec2(60, 480),
                    visual_color=Color(0.12, 0.63, 0.42),
                    shape=PIPE_SHAPE,
                    shape_name="PipeTopBShape",
                ),
                solid_area(
                    "PipeBottomB",
                    position=Vec2(850, 620),
                    visual_size=Vec2(60, 480),
                    visual_color=Color(0.12, 0.63, 0.42),
                    shape=PIPE_SHAPE,
                    shape_name="PipeBottomBShape",
                ),
                Label(
                    "ScoreLabel",
                    text="Score: 0",
                    position=Vec2(24, 22),
                ),
                Label(
                    "StateLabel",
                    text="Space/Up to flap",
                    position=Vec2(158, 330),
                ),
                Timer(
                    "SpawnTimer",
                    wait_time=1.0,
                    autostart=True,
                    signals=[
                        signal("timeout", target=".", method="_on_spawn_timer_timeout"),
                    ],
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
