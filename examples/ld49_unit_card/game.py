from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    Area2D,
    AudioStreamPlayer,
    CollisionShape2D,
    Game,
    Label,
    Node2D,
    Rect2,
    Scene,
    Script,
    StringName,
    Vec2,
    audio_stream,
    node,
    rectangle_shape_2d,
    scene_instance,
    signal,
    sub_resource,
    texture,
)

ROOT = Path(__file__).parent

UNIT_SCRIPT = Script.from_file(
    source="scripts/unit.gd",
    path="res://scripts/unit.gd",
    extends="Area2D",
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
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_window(size=Vec2(320, 240))

unit_scene = Scene(
    path="res://scenes/unit.tscn",
    root=Area2D(
        "Unit",
        script=UNIT_SCRIPT,
        signals=[
            signal("input_event", target=".", method="_on_unit_input_event"),
        ],
        children=[
            node(
                "AnimatedUnit",
                "AnimatedSprite2D",
                sprite_frames=sprite_frames,
                scale=Vec2(3, 3),
            ),
            CollisionShape2D(
                "ClickShape",
                shape=rectangle_shape_2d(size=Vec2(96, 96)),
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

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Node2D(
            "UnitField",
            children=[
                Label(
                    "Hint",
                    text="Click a unit to play its death animation",
                    position=Vec2(36, 28),
                ),
                scene_instance(
                    "UnitA",
                    unit_scene.as_packed_scene(),
                    position=Vec2(80, 128),
                ),
                scene_instance(
                    "UnitB",
                    unit_scene.as_packed_scene(),
                    position=Vec2(160, 128),
                ),
                scene_instance(
                    "UnitC",
                    unit_scene.as_packed_scene(),
                    position=Vec2(240, 128),
                ),
            ],
        ),
    )
)
game.add_scene(unit_scene)

if __name__ == "__main__":
    game.run()
