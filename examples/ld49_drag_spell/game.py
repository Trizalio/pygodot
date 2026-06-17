from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    Color,
    ColorRect,
    Control,
    Game,
    GridContainer,
    HBoxContainer,
    Label,
    Panel,
    Scene,
    Script,
    VBoxContainer,
    Vec2,
    scene_instance,
    signal,
)

ROOT = Path(__file__).parent

MAIN_SCRIPT = Script.from_file(
    source="scripts/main.gd",
    path="res://scripts/main.gd",
    extends="Control",
)
SPELL_SCRIPT = Script.from_file(
    source="scripts/spell.gd",
    path="res://scripts/spell.gd",
    extends="Control",
)
TILE_SCRIPT = Script.from_file(
    source="scripts/tile.gd",
    path="res://scripts/tile.gd",
    extends="Control",
)

game = Game(
    name="LD49DragSpell",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_display(size=Vec2(560, 420), stretch_mode="canvas_items", stretch_aspect="expand")

spell_scene = Scene(
    path="res://scenes/spell.tscn",
    root=Control(
        "Spell",
        script=SPELL_SCRIPT,
        custom_minimum_size=Vec2(116, 72),
        mouse_filter=0,
        children=[
            Panel(
                "Panel",
                anchors_preset=15,
                mouse_filter=2,
                offset_right=116,
                offset_bottom=72,
                children=[
                    ColorRect(
                        "Accent",
                        color=Color(0.25, 0.55, 0.95),
                        custom_minimum_size=Vec2(116, 8),
                        mouse_filter=2,
                    ),
                    Label(
                        "Title",
                        text="Spell",
                        horizontal_alignment=1,
                        vertical_alignment=1,
                        anchors_preset=15,
                        mouse_filter=2,
                        offset_right=116,
                        offset_bottom=72,
                    ),
                ],
            )
        ],
    ),
)

tile_scene = Scene(
    path="res://scenes/tile.tscn",
    root=Control(
        "Tile",
        script=TILE_SCRIPT,
        custom_minimum_size=Vec2(104, 84),
        mouse_filter=0,
        children=[
            Panel(
                "Panel",
                anchors_preset=15,
                mouse_filter=2,
                offset_right=104,
                offset_bottom=84,
                children=[
                    VBoxContainer(
                        "VBox",
                        anchors_preset=15,
                        mouse_filter=2,
                        offset_left=8,
                        offset_top=8,
                        offset_right=96,
                        offset_bottom=76,
                        children=[
                            Label("Title", text="A1", horizontal_alignment=1, mouse_filter=2),
                            Label("State", text="Empty", horizontal_alignment=1, mouse_filter=2),
                        ],
                    )
                ],
            )
        ],
    ),
)

spell_resource = spell_scene.as_packed_scene()
tile_resource = tile_scene.as_packed_scene()

tile_drop_signal = signal("spell_dropped", target=".", method="_on_tile_spell_dropped")

game.add_scene(spell_scene)
game.add_scene(tile_scene)
game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Control(
            "Main",
            script=MAIN_SCRIPT,
            anchors_preset=15,
            offset_right=560,
            offset_bottom=420,
            children=[
                Panel(
                    "Panel",
                    anchors_preset=15,
                    offset_left=20,
                    offset_top=20,
                    offset_right=540,
                    offset_bottom=400,
                    children=[
                        VBoxContainer(
                            "VBox",
                            anchors_preset=15,
                            offset_left=16,
                            offset_top=16,
                            offset_right=504,
                            offset_bottom=364,
                            children=[
                                Label(
                                    "Title",
                                    text="LD49 drag spell slice",
                                    horizontal_alignment=1,
                                    theme_override_font_sizes={"font_size": 24},
                                ),
                                Label("LogLabel", text="Drop a spell onto a tile", horizontal_alignment=1),
                                GridContainer(
                                    "MapGrid",
                                    columns=3,
                                    children=[
                                        scene_instance(
                                            "TileA1",
                                            tile_resource,
                                            tile_id="A1",
                                            signals=[tile_drop_signal],
                                        ),
                                        scene_instance(
                                            "TileA2",
                                            tile_resource,
                                            tile_id="A2",
                                            signals=[tile_drop_signal],
                                        ),
                                        scene_instance(
                                            "TileA3",
                                            tile_resource,
                                            tile_id="A3",
                                            signals=[tile_drop_signal],
                                        ),
                                        scene_instance(
                                            "TileB1",
                                            tile_resource,
                                            tile_id="B1",
                                            signals=[tile_drop_signal],
                                        ),
                                        scene_instance(
                                            "TileB2",
                                            tile_resource,
                                            tile_id="B2",
                                            signals=[tile_drop_signal],
                                        ),
                                        scene_instance(
                                            "TileB3",
                                            tile_resource,
                                            tile_id="B3",
                                            signals=[tile_drop_signal],
                                        ),
                                    ],
                                ),
                                HBoxContainer(
                                    "SpellBar",
                                    children=[
                                        scene_instance(
                                            "SparkSpell",
                                            spell_resource,
                                            spell_id="spark",
                                            display_name="Spark",
                                        ),
                                        scene_instance(
                                            "FreezeSpell",
                                            spell_resource,
                                            spell_id="freeze",
                                            display_name="Freeze",
                                        ),
                                        scene_instance(
                                            "ShieldSpell",
                                            spell_resource,
                                            spell_id="shield",
                                            display_name="Shield",
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                )
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
