from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    Button,
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


def file_script(name: str, *, extends: str = "MarginContainer") -> Script:
    return Script.from_file(
        source=f"scripts/{name}.gd",
        path=f"res://scripts/{name}.gd",
        extends=extends,
    )


game = Game(
    name="LD49SceneFlow",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_display(size=Vec2(540, 750), stretch_mode="canvas_items", stretch_aspect="expand")
game.add_autoload("SceneChanger", "res://scripts/scene_changer.gd")
game.add_autoload("AudioManager", "res://scripts/audio_manager.gd")

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=MarginContainer(
            "Main",
            script=file_script("main"),
            groups=["scene_flow"],
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
                                    text="LD49 Scene Flow",
                                    horizontal_alignment=1,
                                    theme_override_font_sizes={"font_size": 30},
                                ),
                                Label(
                                    "StatusLabel",
                                    text="Waiting",
                                    horizontal_alignment=1,
                                ),
                                Button(
                                    "StartButton",
                                    text="Start Intro",
                                    custom_minimum_size=Vec2(260, 46),
                                    signals=[signal("pressed", target=".", method="_on_start_pressed")],
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
                                Label("Title", text="Intro Scene", horizontal_alignment=1),
                                Label("StatusLabel", text="Arriving", horizontal_alignment=1),
                                Button(
                                    "BackButton",
                                    text="Back To Menu",
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
                                Label("Title", text="Fader Placeholder", horizontal_alignment=1),
                                Label("StatusLabel", text="Fading", horizontal_alignment=1),
                                Button(
                                    "DoneButton",
                                    text="Done",
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
