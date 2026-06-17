from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    AudioStreamPlayer,
    Game,
    Node2D,
    Rect2,
    Scene,
    Script,
    StringName,
    Vec2,
    audio_stream,
    node,
    sub_resource,
    texture,
)

ROOT = Path(__file__).parent

UNIT_SCRIPT = Script.from_file(
    source="scripts/unit.gd",
    path="res://scripts/unit.gd",
    extends="Node2D",
)

frame_idle_0 = sub_resource(
    "AtlasTexture",
    id_hint="unit_idle_0",
    atlas=texture("res://assets/unit_atlas.svg"),
    region=Rect2(0, 0, 32, 32),
)
frame_idle_1 = sub_resource(
    "AtlasTexture",
    id_hint="unit_idle_1",
    atlas=texture("res://assets/unit_atlas.svg"),
    region=Rect2(32, 0, 32, 32),
)
frame_death_0 = sub_resource(
    "AtlasTexture",
    id_hint="unit_death_0",
    atlas=texture("res://assets/unit_atlas.svg"),
    region=Rect2(64, 0, 32, 32),
)
sprite_frames = sub_resource(
    "SpriteFrames",
    id_hint="unit_frames",
    animations=[
        {
            "frames": [
                {"duration": 1.0, "texture": frame_idle_0},
                {"duration": 1.0, "texture": frame_idle_1},
            ],
            "loop": True,
            "name": StringName("idle"),
            "speed": 5.0,
        },
        {
            "frames": [
                {"duration": 1.0, "texture": frame_death_0},
            ],
            "loop": False,
            "name": StringName("death"),
            "speed": 1.0,
        },
    ],
)

game = Game(
    name="LD49UnitCard",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/unit.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_window(size=Vec2(320, 240))

game.add_scene(
    Scene(
        path="res://scenes/unit.tscn",
        root=Node2D(
            "Unit",
            script=UNIT_SCRIPT,
            children=[
                node(
                    "AnimatedUnit",
                    "AnimatedSprite2D",
                    sprite_frames=sprite_frames,
                    position=Vec2(160, 104),
                    scale=Vec2(3, 3),
                ),
                AudioStreamPlayer(
                    "SpawnAudio",
                    stream=audio_stream("res://assets/tone.wav"),
                    volume_db=-8,
                ),
                AudioStreamPlayer(
                    "DeathAudio",
                    stream=audio_stream("res://assets/tone.wav"),
                    volume_db=-12,
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
