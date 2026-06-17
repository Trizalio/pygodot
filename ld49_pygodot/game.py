from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    Button,
    Color,
    ColorRect,
    Game,
    Label,
    MarginContainer,
    Panel,
    Scene,
    Script,
    VBoxContainer,
    Vec2,
    signal,
)

ROOT = Path(__file__).parent


def file_script(name: str) -> Script:
    return Script.from_file(
        source=f"scripts/{name}.gd",
        path=f"res://scripts/{name}.gd",
        extends="MarginContainer",
    )


game = Game(
    name="LD49Pygodot",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_display(size=Vec2(540, 750), stretch_mode="canvas_items", stretch_aspect="expand")
game.set_icon("res://resources/icon.svg")
game.set_project_setting("audio/output_latency/web", 200)
game.set_project_setting("physics/common/enable_pause_aware_picking", True)
game.add_autoload("GameState", "res://scripts/game_state.gd")
game.add_autoload("SceneChanger", "res://scripts/scene_changer.gd")
game.add_autoload("AudioManager", "res://scripts/audio_manager.gd")

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=MarginContainer(
            "Main",
            script=file_script("main"),
            groups=["ld49_port", "stage_a"],
            anchors_preset=15,
            offset_right=540,
            offset_bottom=750,
            children=[
                Panel(
                    "Panel",
                    children=[
                        VBoxContainer(
                            "VBox",
                            children=[
                                Label(
                                    "Title",
                                    text="LD49 pygodot skeleton",
                                    horizontal_alignment=1,
                                    theme_override_font_sizes={"font_size": 30},
                                ),
                                Label(
                                    "StatusLabel",
                                    text="Waiting for Stage A",
                                    horizontal_alignment=1,
                                ),
                                Button(
                                    "IntroButton",
                                    text="Open Intro",
                                    custom_minimum_size=Vec2(260, 46),
                                    signals=[signal("pressed", target=".", method="_on_intro_pressed")],
                                ),
                                Button(
                                    "FaderButton",
                                    text="Preview Fader",
                                    custom_minimum_size=Vec2(260, 46),
                                    signals=[signal("pressed", target=".", method="_on_fader_pressed")],
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
            groups=["ld49_port", "stage_a"],
            anchors_preset=15,
            offset_right=540,
            offset_bottom=750,
            children=[
                Panel(
                    "Panel",
                    children=[
                        VBoxContainer(
                            "VBox",
                            children=[
                                Label("Title", text="Intro Skeleton", horizontal_alignment=1),
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
            groups=["ld49_port", "stage_a"],
            anchors_preset=15,
            offset_right=540,
            offset_bottom=750,
            children=[
                Panel(
                    "Panel",
                    children=[
                        VBoxContainer(
                            "VBox",
                            children=[
                                Label("Title", text="Fader Skeleton", horizontal_alignment=1),
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
