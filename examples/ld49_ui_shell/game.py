from __future__ import annotations

import os
from pathlib import Path

from pygodot import (
    AudioStreamPlayer,
    Button,
    CenterContainer,
    Game,
    HBoxContainer,
    HSeparator,
    Label,
    MarginContainer,
    Panel,
    RichTextLabel,
    Scene,
    Script,
    TextureRect,
    VBoxContainer,
    Vec2,
    signal,
    texture,
)

ROOT = Path(__file__).parent

MAIN_SCRIPT = Script.from_file(
    source="scripts/main.gd",
    path="res://scripts/main.gd",
    extends="MarginContainer",
)

game = Game(
    name="LD49UIShell",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_display(size=Vec2(540, 750), stretch_mode="canvas_items", stretch_aspect="expand")

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=MarginContainer(
            "Main",
            script=MAIN_SCRIPT,
            groups=["ld49_ui_shell"],
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
                                    text="LD49 Tactical Shell",
                                    horizontal_alignment=1,
                                    theme_override_font_sizes={"font_size": 30},
                                ),
                                TextureRect(
                                    "Banner",
                                    texture=texture("res://assets/banner.svg"),
                                    custom_minimum_size=Vec2(480, 160),
                                    expand_mode=1,
                                    stretch_mode=5,
                                ),
                                RichTextLabel(
                                    "Intro",
                                    text=(
                                        "[center]A compact menu shell for the LD49 migration: "
                                        "containers, copied art, buttons, signal binds, and a file-backed script.[/center]"
                                    ),
                                    bbcode_enabled=True,
                                    fit_content=True,
                                    custom_minimum_size=Vec2(480, 96),
                                ),
                                CenterContainer(
                                    "MenuCenter",
                                    children=[
                                        VBoxContainer(
                                            "MenuButtons",
                                            children=[
                                                Button(
                                                    "StartButton",
                                                    text="Start",
                                                    custom_minimum_size=Vec2(260, 46),
                                                    signals=[
                                                        signal(
                                                            "pressed",
                                                            target=".",
                                                            method="_on_menu_action",
                                                            binds=["start"],
                                                        )
                                                    ],
                                                ),
                                                Button(
                                                    "ContinueButton",
                                                    text="Continue",
                                                    custom_minimum_size=Vec2(260, 46),
                                                    signals=[
                                                        signal(
                                                            "pressed",
                                                            target=".",
                                                            method="_on_menu_action",
                                                            binds=["continue"],
                                                        )
                                                    ],
                                                ),
                                                Button(
                                                    "ExitButton",
                                                    text="Exit",
                                                    custom_minimum_size=Vec2(260, 46),
                                                    signals=[
                                                        signal(
                                                            "pressed",
                                                            target=".",
                                                            method="_on_exit_pressed",
                                                        )
                                                    ],
                                                ),
                                            ],
                                        )
                                    ],
                                ),
                                HSeparator("Divider"),
                                HBoxContainer(
                                    "Footer",
                                    children=[
                                        Label("StatusLabel", text="Ready"),
                                        Label("VersionLabel", text="Godot 4 target"),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                AudioStreamPlayer("BackgroundMusic", autoplay=False),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
