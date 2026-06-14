from __future__ import annotations

import os
from pathlib import Path

from pygodot import Color, ColorRect, Game, Label, Node2D, Scene, Script, Timer, Vec2, signal

ROOT = Path(__file__).parent

MAIN_SCRIPT = Script.from_file(
    source="scripts/main.gd",
    path="res://scripts/main.gd",
    extends="Node2D",
)

game = Game(
    name="PygodotTimer",
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
                ColorRect(
                    "Pulse",
                    position=Vec2(270, 125),
                    size=Vec2(100, 100),
                    color=Color(0.2, 0.85, 1.0),
                ),
                Label(
                    "Counter",
                    text="ticks: 0",
                    position=Vec2(285, 245),
                ),
                Timer(
                    "PulseTimer",
                    wait_time=0.5,
                    autostart=True,
                    signals=[
                        signal("timeout", target=".", method="_on_pulse_timer_timeout"),
                    ],
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
