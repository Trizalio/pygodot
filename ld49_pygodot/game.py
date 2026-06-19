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
    RichTextLabel,
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
VIEWPORT_SIZE = Vec2(540, 960)


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

tile_scene = Scene(
    path="res://scenes/tile.tscn",
    root=Panel(
        "Tile",
        script=file_script("tile", extends="Panel"),
        custom_minimum_size=Vec2(92, 92),
        size_flags_horizontal=3,
        size_flags_vertical=3,
        mouse_filter=0,
        children=[
            VBoxContainer(
                "VBox",
                anchors_preset=15,
                mouse_filter=2,
                offset_left=3,
                offset_top=3,
                offset_right=-3,
                offset_bottom=-3,
                children=[
                    Label(
                        "Label",
                        text="A1",
                        custom_minimum_size=Vec2(86, 16),
                        horizontal_alignment=1,
                        mouse_filter=2,
                        clip_text=True,
                        theme_override_font_sizes={"font_size": 11},
                        modulate=Color(0.55, 0.62, 0.67, 1.0),
                    ),
                    Label(
                        "Unit",
                        text="",
                        custom_minimum_size=Vec2(86, 32),
                        horizontal_alignment=1,
                        mouse_filter=2,
                        clip_text=True,
                        theme_override_font_sizes={"font_size": 15},
                    ),
                    Label(
                        "State",
                        text="",
                        custom_minimum_size=Vec2(86, 32),
                        horizontal_alignment=1,
                        mouse_filter=2,
                        clip_text=True,
                        theme_override_font_sizes={"font_size": 13},
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
        custom_minimum_size=Vec2(116, 52),
        size_flags_horizontal=3,
        mouse_filter=0,
        children=[
            VBoxContainer(
                "VBox",
                anchors_preset=15,
                mouse_filter=2,
                offset_left=5,
                offset_top=4,
                offset_right=-5,
                offset_bottom=-4,
                custom_minimum_size=Vec2(104, 42),
                size_flags_horizontal=3,
                children=[
                    Label(
                        "Title",
                        text="Fireball",
                        custom_minimum_size=Vec2(104, 18),
                        size_flags_horizontal=3,
                        horizontal_alignment=1,
                        mouse_filter=2,
                        clip_text=True,
                        theme_override_font_sizes={"font_size": 14},
                    ),
                    Label(
                        "Hint",
                        text="2 dmg + burn",
                        custom_minimum_size=Vec2(104, 18),
                        size_flags_horizontal=3,
                        horizontal_alignment=1,
                        mouse_filter=2,
                        clip_text=True,
                        theme_override_font_sizes={"font_size": 11},
                    ),
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
            display_name="Fire",
            hint_text="2 dmg burn",
        ),
        scene_instance(
            "FrostSpell",
            spell_resource,
            spell_id="frost",
            display_name="Frost",
            hint_text="1 dmg stop",
        ),
        scene_instance(
            "ShieldSpell",
            spell_resource,
            spell_id="shield",
            display_name="Shield",
            hint_text="armor",
        ),
        scene_instance(
            "HealSpell",
            spell_resource,
            spell_id="heal",
            display_name="Heal",
            hint_text="heal",
        ),
    ]


def debug_button(name: str, text: str, method: str) -> Button:
    return Button(
        name,
        text=text,
        custom_minimum_size=Vec2(118, 38),
        size_flags_horizontal=3,
        signals=[signal("pressed", target=".", method=method)],
    )


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
            offset_right=540,
            offset_bottom=960,
            children=[
                TextureRect(
                    "Background",
                    texture=texture("res://resources/icon.svg"),
                    anchors_preset=15,
                    expand_mode=1,
                    stretch_mode=6,
                    modulate=Color(0.18, 0.22, 0.25, 0.25),
                ),
                Panel(
                    "Shell",
                    anchors_preset=15,
                    offset_left=12,
                    offset_top=12,
                    offset_right=-12,
                    offset_bottom=-12,
                    children=[
                        VBoxContainer(
                            "VBox",
                            anchors_preset=15,
                            offset_left=10,
                            offset_top=10,
                            offset_right=-10,
                            offset_bottom=-10,
                            children=[
                                VBoxContainer(
                                    "ScorePanel",
                                    size_flags_horizontal=3,
                                    size_flags_vertical=0,
                                    children=[
                                        Label(
                                            "Title",
                                            text="LD49 battle",
                                            size_flags_horizontal=3,
                                            horizontal_alignment=1,
                                            theme_override_font_sizes={"font_size": 22},
                                        ),
                                        HBoxContainer(
                                            "Counters",
                                            size_flags_horizontal=3,
                                            children=[
                                                Label(
                                                    "ScoreLabel",
                                                    text="Score 0",
                                                    size_flags_horizontal=3,
                                                    horizontal_alignment=1,
                                                ),
                                                Label(
                                                    "TurnLabel",
                                                    text="Turn 1",
                                                    size_flags_horizontal=3,
                                                    horizontal_alignment=1,
                                                ),
                                            ],
                                        ),
                                        Label(
                                            "StatusLabel",
                                            text="LD49 port ready",
                                            size_flags_horizontal=3,
                                            custom_minimum_size=Vec2(0, 38),
                                            horizontal_alignment=1,
                                            autowrap_mode=2,
                                            clip_text=True,
                                        ),
                                    ],
                                ),
                                VBoxContainer(
                                    "BoardPanel",
                                    size_flags_horizontal=3,
                                    size_flags_vertical=3,
                                    size_flags_stretch_ratio=8.0,
                                    children=[
                                        Panel(
                                            "CastlePanel",
                                            size_flags_horizontal=3,
                                            size_flags_vertical=1,
                                            custom_minimum_size=Vec2(0, 48),
                                            children=[
                                                Label(
                                                    "CastleLabel",
                                                    text="Castle 0/6 D:0 U:0 G:0",
                                                    anchors_preset=15,
                                                    offset_left=8,
                                                    offset_top=6,
                                                    offset_right=-8,
                                                    offset_bottom=-6,
                                                    horizontal_alignment=1,
                                                    vertical_alignment=1,
                                                )
                                            ],
                                        ),
                                        GridContainer(
                                            "MapGrid",
                                            columns=5,
                                            size_flags_horizontal=3,
                                            size_flags_vertical=3,
                                            size_flags_stretch_ratio=9.0,
                                            children=map_cells(),
                                        ),
                                    ],
                                ),
                                VBoxContainer(
                                    "ActionsPanel",
                                    size_flags_horizontal=3,
                                    size_flags_vertical=0,
                                    children=[
                                        HBoxContainer(
                                            "SpellsPanel",
                                            size_flags_horizontal=3,
                                            children=spell_buttons(),
                                        ),
                                        Button(
                                            "EventLogButton",
                                            text="Log: ready",
                                            size_flags_horizontal=3,
                                            custom_minimum_size=Vec2(0, 32),
                                            clip_text=True,
                                            signals=[signal("pressed", target=".", method="_on_event_log_button_pressed")],
                                            theme_override_font_sizes={"font_size": 12},
                                        ),
                                        Label(
                                            "HintLine",
                                            text="Drag spell -> unit. Focus events resolve one by one.",
                                            size_flags_horizontal=3,
                                            custom_minimum_size=Vec2(0, 24),
                                            horizontal_alignment=1,
                                            clip_text=True,
                                            theme_override_font_sizes={"font_size": 12},
                                        ),
                                    ],
                                ),
                                HBoxContainer(
                                    "DebugBar",
                                    size_flags_horizontal=3,
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
                                            "Pass Turn",
                                            "_on_advance_units_pressed",
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                ColorRect(
                    "EventLogOverlay",
                    anchors_preset=15,
                    color=Color(0.04, 0.05, 0.06, 0.74),
                    mouse_filter=0,
                    visible=False,
                    signals=[signal("gui_input", target=".", method="_on_event_log_overlay_gui_input")],
                    children=[
                        Panel(
                            "EventLogPanel",
                            anchors_preset=15,
                            offset_left=24,
                            offset_top=72,
                            offset_right=-24,
                            offset_bottom=-72,
                            mouse_filter=0,
                            signals=[signal("gui_input", target=".", method="_on_event_log_panel_gui_input")],
                            children=[
                                VBoxContainer(
                                    "VBox",
                                    anchors_preset=15,
                                    offset_left=12,
                                    offset_top=10,
                                    offset_right=-12,
                                    offset_bottom=-10,
                                    children=[
                                        Label(
                                            "Title",
                                            text="Event Log",
                                            size_flags_horizontal=3,
                                            custom_minimum_size=Vec2(0, 28),
                                            horizontal_alignment=1,
                                            theme_override_font_sizes={"font_size": 18},
                                        ),
                                        RichTextLabel(
                                            "EventLogText",
                                            text="",
                                            size_flags_horizontal=3,
                                            size_flags_vertical=3,
                                            autowrap_mode=2,
                                            scroll_active=True,
                                            fit_content=False,
                                            mouse_filter=0,
                                            theme_override_font_sizes={"normal_font_size": 14},
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
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
            offset_right=540,
            offset_bottom=960,
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
            offset_right=540,
            offset_bottom=960,
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
            offset_right=540,
            offset_bottom=960,
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
