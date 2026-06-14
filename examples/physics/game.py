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

PROBE_SHAPE = rectangle_shape_2d(size=Vec2(64, 64))
GOAL_SHAPE = rectangle_shape_2d(size=Vec2(90, 90))

game = Game(
    name="PygodotPhysics",
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
                    "Status",
                    text="waiting for area_entered",
                    position=Vec2(215, 70),
                ),
                Area2D(
                    "Probe",
                    position=Vec2(130, 180),
                    signals=[
                        signal("area_entered", target=".", method="_on_probe_area_entered"),
                    ],
                    children=[
                        ColorRect(
                            "ProbeVisual",
                            position=Vec2(-32, -32),
                            size=Vec2(64, 64),
                            color=Color(0.2, 0.85, 1.0),
                        ),
                        CollisionShape2D("ProbeShape", shape=PROBE_SHAPE),
                    ],
                ),
                Area2D(
                    "Goal",
                    position=Vec2(320, 180),
                    children=[
                        ColorRect(
                            "GoalVisual",
                            position=Vec2(-45, -45),
                            size=Vec2(90, 90),
                            color=Color(1.0, 0.68, 0.25, 0.55),
                        ),
                        CollisionShape2D("GoalShape", shape=GOAL_SHAPE),
                    ],
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
