from __future__ import annotations

import unittest

from pygodot import Color
from pygodot.emitters.tres import TresEmitter
from pygodot.ir.model import IRExternalResource, IRExternalResourceRef, IRGeneratedResource


class TresEmitterTests(unittest.TestCase):
    def test_tres_emitter_snapshot_with_label_settings(self) -> None:
        resource = IRGeneratedResource(
            type="LabelSettings",
            path="res://ui/title_label_settings.tres",
            id="LabelSettings_ui_title_label_settings_tres",
            props={
                "font_color": Color(1, 1, 1),
                "font_size": 32,
            },
        )

        self.assertEqual(
            TresEmitter().emit(resource),
            """[gd_resource type="LabelSettings" format=3]

[resource]
font_color = Color(1, 1, 1, 1.0)
font_size = 32
""",
        )

    def test_tres_emitter_snapshot_with_label_settings_font_resource(self) -> None:
        resource = IRGeneratedResource(
            type="LabelSettings",
            path="res://ui/title_label_settings.tres",
            id="LabelSettings_ui_title_label_settings_tres",
            props={
                "font": IRExternalResourceRef("Font_assets_display_ttf"),
                "font_color": Color(1, 1, 1),
                "font_size": 32,
            },
            external_resources=(
                IRExternalResource(
                    type="Font",
                    path="res://assets/display.ttf",
                    id="Font_assets_display_ttf",
                ),
            ),
        )

        self.assertEqual(
            TresEmitter().emit(resource),
            """[gd_resource type="LabelSettings" load_steps=2 format=3]

[ext_resource type="Font" path="res://assets/display.ttf" id="Font_assets_display_ttf"]

[resource]
font = ExtResource("Font_assets_display_ttf")
font_color = Color(1, 1, 1, 1.0)
font_size = 32
""",
        )

    def test_tres_emitter_snapshot_with_style_box_flat(self) -> None:
        resource = IRGeneratedResource(
            type="StyleBoxFlat",
            path="res://ui/panel_style.tres",
            id="StyleBoxFlat_ui_panel_style_tres",
            props={
                "bg_color": Color(0.1, 0.2, 0.3),
                "border_color": Color(0.4, 0.5, 0.6),
                "border_width_bottom": 2,
                "border_width_left": 2,
                "border_width_right": 2,
                "border_width_top": 2,
                "corner_radius_bottom_left": 6,
                "corner_radius_bottom_right": 6,
                "corner_radius_top_left": 6,
                "corner_radius_top_right": 6,
            },
        )

        self.assertEqual(
            TresEmitter().emit(resource),
            """[gd_resource type="StyleBoxFlat" format=3]

[resource]
bg_color = Color(0.1, 0.2, 0.3, 1.0)
border_color = Color(0.4, 0.5, 0.6, 1.0)
border_width_bottom = 2
border_width_left = 2
border_width_right = 2
border_width_top = 2
corner_radius_bottom_left = 6
corner_radius_bottom_right = 6
corner_radius_top_left = 6
corner_radius_top_right = 6
""",
        )
