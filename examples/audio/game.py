from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    AudioStreamPlayer,
    Button,
    Color,
    ColorRect,
    Game,
    Label,
    Node2D,
    Scene,
    Script,
    Vec2,
    audio_stream,
    signal,
)

ROOT = Path(__file__).parent

MAIN_SCRIPT = Script.from_file(
    source="scripts/main.gd",
    path="res://scripts/main.gd",
    extends="Node2D",
)

game = Game(
    name="PygodotAudio",
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
                    "Title",
                    text="Audio resource copied from source_root",
                    position=Vec2(180, 90),
                ),
                Label(
                    "Status",
                    text="ready",
                    position=Vec2(292, 145),
                ),
                Button(
                    "PlayButton",
                    text="Play tone",
                    position=Vec2(255, 205),
                    size=Vec2(130, 44),
                    signals=[
                        signal("pressed", target=".", method="_on_play_button_pressed"),
                    ],
                ),
                AudioStreamPlayer(
                    "Player",
                    stream=audio_stream("res://assets/tone.wav"),
                    volume_db=-8,
                    signals=[
                        signal("finished", target=".", method="_on_player_finished"),
                    ],
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
