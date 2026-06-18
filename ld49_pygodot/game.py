from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    Button,
    Color,
    ColorRect,
    Game,
    GridContainer,
    HBoxContainer,
    Label,
    MarginContainer,
    Panel,
    Scene,
    Script,
    TextureRect,
    VBoxContainer,
    Vec2,
    scene_instance,
    signal,
    texture,
)

ROOT = Path(__file__).parent
VIEWPORT_SIZE = Vec2(820, 760)


def file_script(name: str, *, extends: str = "MarginContainer") -> Script:
    return Script.from_file(
        source=f"scripts/{name}.gd",
        path=f"res://scripts/{name}.gd",
        extends=extends,
    )


game = Game(
    name="LD49Pygodot",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_display(size=VIEWPORT_SIZE, stretch_mode="canvas_items", stretch_aspect="expand")
game.set_icon("res://resources/icon.svg")
game.set_project_setting("audio/output_latency/web", 200)
game.set_project_setting("physics/common/enable_pause_aware_picking", True)
game.add_autoload("Matrix", "res://scripts/matrix.gd")
game.add_autoload("MatrixUtils", "res://scripts/matrix_utils.gd")
game.add_autoload("Rand", "res://scripts/rand.gd")
game.add_autoload("Utils", "res://scripts/utils.gd")
game.add_autoload("GameState", "res://scripts/game_state.gd")
game.add_autoload("SceneChanger", "res://scripts/scene_changer.gd")
game.add_autoload("AudioManager", "res://scripts/audio_manager.gd")

hint_scene = Scene(
    path="res://scenes/hint.tscn",
    root=Panel(
        "Hint",
        custom_minimum_size=Vec2(360, 92),
        children=[
            VBoxContainer(
                "VBox",
                anchors_preset=15,
                offset_left=10,
                offset_top=8,
                offset_right=350,
                offset_bottom=84,
                children=[
                    Label("Title", text="Hint", horizontal_alignment=1),
                    Label(
                        "Body",
                        text="Drag spells onto units, advance turns, and clear the unstable board.",
                        custom_minimum_size=Vec2(340, 48),
                        horizontal_alignment=1,
                        autowrap_mode=2,
                        clip_text=True,
                    ),
                ],
            )
        ],
    ),
)
hint_resource = hint_scene.as_packed_scene()

tile_scene = Scene(
    path="res://scenes/tile.tscn",
    root=Panel(
        "Tile",
        script=file_script("tile", extends="Panel"),
        custom_minimum_size=Vec2(66, 56),
        mouse_filter=0,
        children=[
            VBoxContainer(
                "VBox",
                anchors_preset=15,
                mouse_filter=2,
                offset_left=4,
                offset_top=4,
                offset_right=62,
                offset_bottom=52,
                children=[
                    Label(
                        "Label",
                        text="A1",
                        custom_minimum_size=Vec2(58, 20),
                        horizontal_alignment=1,
                        mouse_filter=2,
                        clip_text=True,
                    ),
                    Label(
                        "State",
                        text="Empty",
                        custom_minimum_size=Vec2(58, 24),
                        horizontal_alignment=1,
                        mouse_filter=2,
                        clip_text=True,
                    ),
                ],
            )
        ],
    ),
)
tile_resource = tile_scene.as_packed_scene()

spell_scene = Scene(
    path="res://scenes/spell.tscn",
    root=Panel(
        "Spell",
        script=file_script("spell", extends="Panel"),
        custom_minimum_size=Vec2(180, 58),
        mouse_filter=0,
        children=[
            VBoxContainer(
                "VBox",
                anchors_preset=15,
                mouse_filter=2,
                offset_left=8,
                offset_top=6,
                offset_right=172,
                offset_bottom=52,
                children=[
                    Label("Title", text="Fireball", horizontal_alignment=1, mouse_filter=2),
                    Label("Hint", text="2 damage + burn", horizontal_alignment=1, mouse_filter=2),
                ],
            )
        ],
    ),
)
spell_resource = spell_scene.as_packed_scene()

unit_scene = Scene(
    path="res://scenes/unit.tscn",
    root=Panel(
        "Unit",
        script=file_script("unit", extends="Panel"),
        custom_minimum_size=Vec2(180, 66),
        children=[
            VBoxContainer(
                "VBox",
                anchors_preset=15,
                mouse_filter=2,
                offset_left=8,
                offset_top=6,
                offset_right=172,
                offset_bottom=60,
                children=[
                    Label("Name", text="Unit", horizontal_alignment=1, mouse_filter=2),
                    Label("Stats", text="HP 1", horizontal_alignment=1, mouse_filter=2),
                    Label("Status", text="ready", horizontal_alignment=1, mouse_filter=2),
                ],
            )
        ],
    ),
)
unit_resource = unit_scene.as_packed_scene()


def map_cells() -> list:
    cells = []
    for row in "ABCDE":
        for column in range(1, 6):
            cell_id = f"{row}{column}"
            cells.append(
                scene_instance(
                    f"Tile{cell_id}",
                    tile_resource,
                    tile_id=cell_id,
                )
            )
    return cells


def spell_buttons() -> list:
    return [
        scene_instance(
            "FireballSpell",
            spell_resource,
            spell_id="fireball",
            display_name="Fireball",
            hint_text="2 damage + burn",
        ),
        scene_instance(
            "FrostSpell",
            spell_resource,
            spell_id="frost",
            display_name="Frost",
            hint_text="1 damage + freeze",
        ),
        scene_instance(
            "ShieldSpell",
            spell_resource,
            spell_id="shield",
            display_name="Shield",
            hint_text="add armor",
        ),
        scene_instance(
            "HealSpell",
            spell_resource,
            spell_id="heal",
            display_name="Heal",
            hint_text="restore hp",
        ),
    ]


def debug_button(name: str, text: str, method: str) -> Button:
    return Button(
        name,
        text=text,
        custom_minimum_size=Vec2(170, 42),
        signals=[signal("pressed", target=".", method=method)],
    )


def unit_cards() -> list:
    return [
        scene_instance(
            "ImpUnit",
            unit_resource,
            unit_id="imp",
            display_name="Imp",
            faction="demon",
            cell_id="A1",
            hp=4,
        ),
        scene_instance(
            "BonesUnit",
            unit_resource,
            unit_id="bones",
            display_name="Bones",
            faction="undead",
            cell_id="C3",
            hp=5,
        ),
        scene_instance(
            "GobUnit",
            unit_resource,
            unit_id="gob",
            display_name="Gob",
            faction="greenskin",
            cell_id="E1",
            hp=3,
        ),
    ]


game.add_scene(hint_scene)
game.add_scene(tile_scene)
game.add_scene(spell_scene)
game.add_scene(unit_scene)

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=MarginContainer(
            "Main",
            script=file_script("main"),
            groups=["ld49_port", "stage_a_g"],
            anchors_preset=15,
            offset_right=820,
            offset_bottom=760,
            children=[
                TextureRect(
                    "Background",
                    texture=texture("res://resources/icon.svg"),
                    anchors_preset=15,
                    offset_right=820,
                    offset_bottom=760,
                    expand_mode=1,
                    stretch_mode=6,
                    modulate=Color(0.18, 0.22, 0.25, 0.25),
                ),
                Panel(
                    "Shell",
                    anchors_preset=15,
                    offset_left=18,
                    offset_top=18,
                    offset_right=802,
                    offset_bottom=742,
                    children=[
                        VBoxContainer(
                            "VBox",
                            anchors_preset=15,
                            offset_left=14,
                            offset_top=14,
                            offset_right=770,
                            offset_bottom=710,
                            children=[
                                HBoxContainer(
                                    "ScorePanel",
                                    children=[
                                        Label(
                                            "Title",
                                            text="LD49 battle",
                                            custom_minimum_size=Vec2(190, 34),
                                            theme_override_font_sizes={"font_size": 22},
                                        ),
                                        Label(
                                            "ScoreLabel",
                                            text="Score 0",
                                            custom_minimum_size=Vec2(115, 34),
                                            horizontal_alignment=1,
                                        ),
                                        Label(
                                            "TurnLabel",
                                            text="Turn 1",
                                            custom_minimum_size=Vec2(100, 34),
                                            horizontal_alignment=1,
                                        ),
                                        Label(
                                            "StatusLabel",
                                            text="LD49 port ready",
                                            custom_minimum_size=Vec2(330, 34),
                                            horizontal_alignment=1,
                                        ),
                                    ],
                                ),
                                HBoxContainer(
                                    "GameBody",
                                    children=[
                                        GridContainer(
                                            "MapGrid",
                                            columns=5,
                                            custom_minimum_size=Vec2(360, 310),
                                            children=map_cells(),
                                        ),
                                        VBoxContainer(
                                            "SidePanel",
                                            custom_minimum_size=Vec2(390, 540),
                                            children=[
                                                Label("SpellsTitle", text="Spells", horizontal_alignment=1),
                                                GridContainer("SpellsPanel", columns=2, children=spell_buttons()),
                                                Label("UnitsTitle", text="Units", horizontal_alignment=1),
                                                VBoxContainer("UnitsPanel", children=unit_cards()),
                                                Label("HintsTitle", text="Hints", horizontal_alignment=1),
                                                scene_instance("HintPanel", hint_resource),
                                            ],
                                        ),
                                    ],
                                ),
                                HBoxContainer(
                                    "DebugBar",
                                    children=[
                                        debug_button(
                                            "IntroButton",
                                            "Open Intro",
                                            "_on_intro_pressed",
                                        ),
                                        debug_button(
                                            "FaderButton",
                                            "Preview Fader",
                                            "_on_fader_pressed",
                                        ),
                                        debug_button(
                                            "ResetButton",
                                            "Reset State",
                                            "_on_reset_pressed",
                                        ),
                                        debug_button(
                                            "AdvanceUnitsButton",
                                            "Advance Units",
                                            "_on_advance_units_pressed",
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

game.add_scene(
    Scene(
        path="res://scenes/end.tscn",
        root=MarginContainer(
            "End",
            script=file_script("end"),
            groups=["ld49_port", "stage_f"],
            anchors_preset=15,
            offset_right=820,
            offset_bottom=760,
            children=[
                Panel(
                    "Panel",
                    children=[
                        VBoxContainer(
                            "VBox",
                            children=[
                                Label("Title", text="Battle Complete", horizontal_alignment=1),
                                Label("StatusLabel", text="All unstable units defeated", horizontal_alignment=1),
                                Button(
                                    "BackButton",
                                    text="Back To Main",
                                    custom_minimum_size=Vec2(260, 46),
                                    signals=[signal("pressed", target=".", method="_on_back_pressed")],
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
        path="res://scenes/intro.tscn",
        root=MarginContainer(
            "Intro",
            script=file_script("intro"),
            groups=["ld49_port", "stage_a_g"],
            anchors_preset=15,
            offset_right=820,
            offset_bottom=760,
            children=[
                Panel(
                    "Panel",
                    children=[
                        VBoxContainer(
                            "VBox",
                            children=[
                                Label("Title", text="Intro", horizontal_alignment=1),
                                Label("StatusLabel", text="Intro placeholder", horizontal_alignment=1),
                                Button(
                                    "BackButton",
                                    text="Back To Main",
                                    custom_minimum_size=Vec2(260, 46),
                                    signals=[signal("pressed", target=".", method="_on_back_pressed")],
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
        path="res://scenes/fader.tscn",
        root=MarginContainer(
            "Fader",
            script=file_script("fader"),
            groups=["ld49_port", "stage_a_g"],
            anchors_preset=15,
            offset_right=820,
            offset_bottom=760,
            children=[
                Panel(
                    "Panel",
                    children=[
                        VBoxContainer(
                            "VBox",
                            children=[
                                Label("Title", text="Fader", horizontal_alignment=1),
                                Label("StatusLabel", text="Fader placeholder", horizontal_alignment=1),
                                ColorRect(
                                    "FadePreview",
                                    custom_minimum_size=Vec2(260, 120),
                                    color=Color(0, 0, 0, 0.7),
                                ),
                                Button(
                                    "DoneButton",
                                    text="Back To Main",
                                    custom_minimum_size=Vec2(260, 46),
                                    signals=[signal("pressed", target=".", method="_on_done_pressed")],
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
