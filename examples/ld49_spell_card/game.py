from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    Color,
    ColorRect,
    Game,
    Label,
    Node2D,
    Scene,
    Vec2,
    ext_resource,
    shader,
    sub_resource,
)

ROOT = Path(__file__).parent

SPELL_SHADER = shader("res://shaders/spell_pulse.gdshader")

generated_spell_material = sub_resource(
    "ShaderMaterial",
    id_hint="arcane_burst",
    shader=SPELL_SHADER,
    **{
        "shader_parameter/pulse": 0.65,
        "shader_parameter/tint": Color(0.2, 0.85, 1.0),
    },
)

external_spell_material = ext_resource(
    "res://materials/spell_edge.tres",
    type="ShaderMaterial",
)

game = Game(
    name="LD49SpellCard",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_window(size=Vec2(360, 220))

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Node2D(
            "SpellBench",
            children=[
                Label(
                    "Title",
                    text="ShaderMaterial spell visuals",
                    position=Vec2(48, 24),
                ),
                ColorRect(
                    "GeneratedMaterialSpell",
                    color=Color(1, 1, 1),
                    material=generated_spell_material,
                    position=Vec2(64, 76),
                    size=Vec2(96, 96),
                ),
                ColorRect(
                    "ExternalMaterialSpell",
                    color=Color(1, 1, 1),
                    material=external_spell_material,
                    position=Vec2(200, 76),
                    size=Vec2(96, 96),
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
