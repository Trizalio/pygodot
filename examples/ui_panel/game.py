from __future__ import annotations

import os
from pathlib import Path

from pygodot import Button, Color, ColorRect, Control, Game, Label, Scene, Vec2, font, label_settings

ROOT = Path(__file__).parent
EXAMPLES_ROOT = ROOT.parent

game = Game(
    name="PygodotUIPanel",
    source_root=EXAMPLES_ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/main.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)
game.set_window(size=Vec2(720, 480))

title_settings = label_settings(
    "res://ui/title_label_settings.tres",
    font=font("res://font/assets/WDXL_Lubrifont_TC/WDXLLubrifontTC-Regular.ttf"),
    font_size=34,
    font_color=Color(0.92, 0.98, 1.0),
)
section_settings = label_settings(
    "res://ui/section_label_settings.tres",
    font_size=18,
    font_color=Color(0.62, 0.82, 0.88),
)

game.add_scene(
    Scene(
        path="res://scenes/main.tscn",
        root=Control(
            "Dashboard",
            children=[
                ColorRect(
                    "Background",
                    position=Vec2(0, 0),
                    size=Vec2(720, 480),
                    color=Color(0.035, 0.045, 0.055),
                ),
                ColorRect(
                    "HeaderBand",
                    position=Vec2(0, 0),
                    size=Vec2(720, 88),
                    color=Color(0.08, 0.12, 0.16),
                ),
                Label(
                    "Title",
                    text="Mission Control",
                    position=Vec2(36, 22),
                    label_settings=title_settings,
                ),
                Label(
                    "Subtitle",
                    text="Static UI generated from Python objects",
                    position=Vec2(39, 61),
                    theme_override_font_sizes={"font_size": 15},
                    theme_override_colors={"font_color": Color(0.7, 0.77, 0.82)},
                ),
                ColorRect(
                    "StatusPanel",
                    position=Vec2(32, 118),
                    size=Vec2(312, 238),
                    color=Color(0.1, 0.13, 0.15),
                ),
                Label(
                    "StatusHeading",
                    text="SYSTEM STATUS",
                    position=Vec2(56, 142),
                    label_settings=section_settings,
                ),
                Label(
                    "PowerLabel",
                    text="Power",
                    position=Vec2(58, 188),
                    theme_override_font_sizes={"font_size": 16},
                    theme_override_colors={"font_color": Color(0.74, 0.8, 0.84)},
                ),
                Label(
                    "PowerValue",
                    text="97%",
                    position=Vec2(264, 188),
                    theme_override_font_sizes={"font_size": 18},
                    theme_override_colors={"font_color": Color(0.65, 1.0, 0.78)},
                ),
                Label(
                    "SignalLabel",
                    text="Signal",
                    position=Vec2(58, 230),
                    theme_override_font_sizes={"font_size": 16},
                    theme_override_colors={"font_color": Color(0.74, 0.8, 0.84)},
                ),
                Label(
                    "SignalValue",
                    text="Stable",
                    position=Vec2(236, 230),
                    theme_override_font_sizes={"font_size": 18},
                    theme_override_colors={"font_color": Color(0.65, 1.0, 0.78)},
                ),
                Label(
                    "QueueLabel",
                    text="Queue",
                    position=Vec2(58, 272),
                    theme_override_font_sizes={"font_size": 16},
                    theme_override_colors={"font_color": Color(0.74, 0.8, 0.84)},
                ),
                Label(
                    "QueueValue",
                    text="14 tasks",
                    position=Vec2(224, 272),
                    theme_override_font_sizes={"font_size": 18},
                    theme_override_colors={"font_color": Color(0.92, 0.88, 0.58)},
                ),
                ColorRect(
                    "ActionPanel",
                    position=Vec2(376, 118),
                    size=Vec2(312, 238),
                    color=Color(0.085, 0.1, 0.13),
                ),
                Label(
                    "ActionHeading",
                    text="ACTIONS",
                    position=Vec2(400, 142),
                    label_settings=section_settings,
                ),
                Button(
                    "PrimaryAction",
                    text="Deploy",
                    position=Vec2(400, 188),
                    size=Vec2(126, 42),
                ),
                Button(
                    "SecondaryAction",
                    text="Schedule",
                    position=Vec2(542, 188),
                    size=Vec2(122, 42),
                ),
                Button(
                    "QuietAction",
                    text="View Logs",
                    position=Vec2(400, 248),
                    size=Vec2(264, 42),
                ),
                Label(
                    "Hint",
                    text="Buttons are static here; scripts can wire behavior later.",
                    position=Vec2(402, 312),
                    theme_override_font_sizes={"font_size": 14},
                    theme_override_colors={"font_color": Color(0.62, 0.68, 0.72)},
                ),
                ColorRect(
                    "FooterBand",
                    position=Vec2(32, 386),
                    size=Vec2(656, 54),
                    color=Color(0.065, 0.075, 0.09),
                ),
                Label(
                    "Footer",
                    text="Generated LabelSettings resources keep typography reusable.",
                    position=Vec2(56, 404),
                    theme_override_font_sizes={"font_size": 16},
                    theme_override_colors={"font_color": Color(0.74, 0.82, 0.86)},
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
