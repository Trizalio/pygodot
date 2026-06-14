from __future__ import annotations

import unittest

from pygodot import Node2D, Rect2, Scene, Script, ext_resource
from pygodot.emitters.tscn import TscnEmitter
from pygodot.ir.normalize import normalize_scene
from tests.helpers import make_scene


class TscnEmitterTests(unittest.TestCase):
    def test_tscn_emitter_snapshot(self) -> None:
        scene = normalize_scene(make_scene())

        self.assertEqual(
            TscnEmitter().emit(scene),
            """[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://scripts/main.gd" id="Script_scripts_main_gd"]

[node name="Main" type="Node2D"]
script = ExtResource("Script_scripts_main_gd")

[node name="Title" type="Label" parent="."]
position = Vector2(80, 60)
text = "Generated scene"

[node name="StartButton" type="Button" parent="."]
position = Vector2(80, 120)
text = "Click me"


[connection signal="pressed" from="StartButton" to="." method="_on_start_pressed"]
""",
        )

    def test_tscn_emitter_snapshot_with_external_resource_property(self) -> None:
        scene = normalize_scene(
            Scene(
                path="res://scenes/main.tscn",
                root=Node2D(
                    "Main",
                    icon=ext_resource("res://assets/icon.svg", type="Texture2D"),
                ),
            )
        )

        self.assertEqual(
            TscnEmitter().emit(scene),
            """[gd_scene load_steps=2 format=3]

[ext_resource type="Texture2D" path="res://assets/icon.svg" id="Texture2D_assets_icon_svg"]

[node name="Main" type="Node2D"]
icon = ExtResource("Texture2D_assets_icon_svg")
""",
        )

    def test_tscn_emitter_snapshot_with_rect2_property(self) -> None:
        scene = normalize_scene(
            Scene(
                path="res://scenes/main.tscn",
                root=Node2D(
                    "Main",
                    region_rect=Rect2(0, 0, 16, 32),
                ),
            )
        )

        self.assertEqual(
            TscnEmitter().emit(scene),
            """[gd_scene format=3]

[node name="Main" type="Node2D"]
region_rect = Rect2(0, 0, 16, 32)
""",
        )

    def test_tscn_emitter_snapshot_with_referenced_script(self) -> None:
        scene = normalize_scene(
            Scene(
                path="res://scenes/main.tscn",
                root=Node2D(
                    "Main",
                    script=Script.reference(
                        "res://manual/player.gd",
                        extends="Node2D",
                    ),
                ),
            )
        )

        self.assertEqual(
            TscnEmitter().emit(scene),
            """[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://manual/player.gd" id="Script_manual_player_gd"]

[node name="Main" type="Node2D"]
script = ExtResource("Script_manual_player_gd")
""",
        )
