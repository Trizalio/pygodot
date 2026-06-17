from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    Button,
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
    TextureRect,
    VBoxContainer,
    Vec2,
    scene_instance,
    signal,
    style_box_flat,
    texture,
)

ROOT = Path(__file__).parent


def file_script(name: str, *, extends: str = "Control") -> Script:
    return Script.from_file(
        source=f"scripts/{name}.gd",
        path=f"res://scripts/{name}.gd",
        extends=extends,
    )


PANEL_STYLE = style_box_flat(
    "res://ui/panel_style.tres",
    bg_color=Color(0.07, 0.09, 0.11),
    border_color=Color(0.24, 0.42, 0.52),
    border_width_all=2,
    corner_radius_all=6,
)

UNIT_TEXTURE = texture("res://assets/unit.svg")

game = Game(
    name="LD49VerticalSlice",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/menu.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_display(size=Vec2(760, 560), stretch_mode="canvas_items", stretch_aspect="expand")
game.set_icon("res://assets/unit.svg")
game.add_autoload("GameState", "res://scripts/game_state.gd")
game.add_autoload("SceneChanger", "res://scripts/scene_changer.gd")
game.add_autoload("AudioManager", "res://scripts/audio_manager.gd")
game.add_input_action("restart", keys=["R"])

spell_scene = Scene(
    path="res://scenes/spell.tscn",
    root=Control(
        "Spell",
        script=file_script("spell"),
        custom_minimum_size=Vec2(128, 74),
        mouse_filter=0,
        children=[
            Panel(
                "Panel",
                anchors_preset=15,
                mouse_filter=2,
                offset_right=128,
                offset_bottom=74,
                theme_override_styles={"panel": PANEL_STYLE},
                children=[
                    VBoxContainer(
                        "VBox",
                        anchors_preset=15,
                        mouse_filter=2,
                        offset_left=8,
                        offset_top=8,
                        offset_right=120,
                        offset_bottom=66,
                        children=[
                            Label(
                                "Title",
                                text="Spark",
                                horizontal_alignment=1,
                                mouse_filter=2,
                            ),
                            Label(
                                "Hint",
                                text="drag",
                                horizontal_alignment=1,
                                mouse_filter=2,
                            ),
                        ],
                    )
                ],
            )
        ],
    ),
)

tile_scene = Scene(
    path="res://scenes/tile.tscn",
    root=Control(
        "Tile",
        script=file_script("tile"),
        custom_minimum_size=Vec2(82, 58),
        mouse_filter=0,
        children=[
            Panel(
                "Panel",
                anchors_preset=15,
                mouse_filter=2,
                offset_right=82,
                offset_bottom=58,
                children=[
                    VBoxContainer(
                        "VBox",
                        anchors_preset=15,
                        mouse_filter=2,
                        offset_left=5,
                        offset_top=5,
                        offset_right=77,
                        offset_bottom=53,
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

unit_scene = Scene(
    path="res://scenes/unit.tscn",
    root=Control(
        "Unit",
        script=file_script("unit"),
        custom_minimum_size=Vec2(132, 154),
        children=[
            Panel(
                "Panel",
                anchors_preset=15,
                offset_right=132,
                offset_bottom=154,
                theme_override_styles={"panel": PANEL_STYLE},
                children=[
                    VBoxContainer(
                        "VBox",
                        anchors_preset=15,
                        offset_left=10,
                        offset_top=10,
                        offset_right=122,
                        offset_bottom=144,
                        children=[
                            Label("Title", text="Scout", horizontal_alignment=1),
                            TextureRect(
                                "Portrait",
                                texture=UNIT_TEXTURE,
                                custom_minimum_size=Vec2(96, 96),
                                expand_mode=1,
                                stretch_mode=5,
                            ),
                            Label("Status", text="1 unit", horizontal_alignment=1),
                        ],
                    )
                ],
            )
        ],
    ),
)

spell_resource = spell_scene.as_packed_scene()
tile_resource = tile_scene.as_packed_scene()
unit_resource = unit_scene.as_packed_scene()
tile_drop_signal = signal("spell_dropped", target=".", method="_on_tile_spell_dropped")


def tile_instances() -> list:
    tiles = []
    for row in "ABCDE":
        for column in range(1, 6):
            tile_id = f"{row}{column}"
            tiles.append(
                scene_instance(
                    f"Tile{tile_id}",
                    tile_resource,
                    tile_id=tile_id,
                    signals=[tile_drop_signal],
                )
            )
    return tiles


game.add_scene(spell_scene)
game.add_scene(tile_scene)
game.add_scene(unit_scene)

game.add_scene(
    Scene(
        path="res://scenes/menu.tscn",
        root=Control(
            "Menu",
            script=file_script("menu"),
            anchors_preset=15,
            offset_right=760,
            offset_bottom=560,
            children=[
                Panel(
                    "Panel",
                    anchors_preset=15,
                    offset_left=160,
                    offset_top=120,
                    offset_right=600,
                    offset_bottom=420,
                    theme_override_styles={"panel": PANEL_STYLE},
                    children=[
                        VBoxContainer(
                            "VBox",
                            anchors_preset=15,
                            offset_left=24,
                            offset_top=24,
                            offset_right=416,
                            offset_bottom=276,
                            children=[
                                Label(
                                    "Title",
                                    text="LD49 vertical slice",
                                    horizontal_alignment=1,
                                    theme_override_font_sizes={"font_size": 28},
                                ),
                                Label(
                                    "StatusLabel",
                                    text="Ready",
                                    horizontal_alignment=1,
                                ),
                                Button(
                                    "StartButton",
                                    text="Start battle",
                                    custom_minimum_size=Vec2(260, 46),
                                    signals=[signal("pressed", target=".", method="_on_start_pressed")],
                                ),
                            ],
                        )
                    ],
                )
            ],
        ),
    )
)

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Control(
            "Main",
            script=file_script("main"),
            anchors_preset=15,
            offset_right=760,
            offset_bottom=560,
            children=[
                ColorRect(
                    "Background",
                    anchors_preset=15,
                    offset_right=760,
                    offset_bottom=560,
                    color=Color(0.03, 0.04, 0.05),
                ),
                Panel(
                    "Panel",
                    anchors_preset=15,
                    offset_left=18,
                    offset_top=18,
                    offset_right=742,
                    offset_bottom=542,
                    theme_override_styles={"panel": PANEL_STYLE},
                    children=[
                        VBoxContainer(
                            "VBox",
                            anchors_preset=15,
                            offset_left=16,
                            offset_top=16,
                            offset_right=708,
                            offset_bottom=508,
                            children=[
                                HBoxContainer(
                                    "Header",
                                    children=[
                                        Label(
                                            "Title",
                                            text="Battle rehearsal",
                                            theme_override_font_sizes={"font_size": 24},
                                        ),
                                        Label(
                                            "LogLabel",
                                            text="Drag Spark onto any tile",
                                            horizontal_alignment=1,
                                            custom_minimum_size=Vec2(360, 32),
                                        ),
                                        Button(
                                            "BackButton",
                                            text="Menu",
                                            custom_minimum_size=Vec2(96, 36),
                                            signals=[signal("pressed", target=".", method="_on_back_pressed")],
                                        ),
                                    ],
                                ),
                                HBoxContainer(
                                    "BoardRow",
                                    children=[
                                        GridContainer(
                                            "MapGrid",
                                            columns=5,
                                            children=tile_instances(),
                                        ),
                                        VBoxContainer(
                                            "UnitColumn",
                                            children=[
                                                scene_instance(
                                                    "UnitScout",
                                                    unit_resource,
                                                    unit_name="Scout",
                                                ),
                                            ],
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
                                            "GuardSpell",
                                            spell_resource,
                                            spell_id="guard",
                                            display_name="Guard",
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
