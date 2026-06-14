from __future__ import annotations

import unittest

from pygodot import (
    CollisionShape2D,
    Node,
    Node2D,
    Scene,
    Vec2,
    audio_stream,
    ext_resource,
    font,
    packed_scene,
    rectangle_shape_2d,
    texture,
)
from pygodot.ir.normalize import normalize_scene


class NormalizeTests(unittest.TestCase):
    def test_normalize_collects_external_resource_properties(self) -> None:
        scene = normalize_scene(
            Scene(
                path="res://scenes/main.tscn",
                root=Node2D(
                    "Main",
                    icon=ext_resource("res://assets/icon.svg", type="Texture2D"),
                ),
            )
        )

        self.assertEqual(len(scene.external_resources), 1)
        resource = scene.external_resources[0]
        self.assertEqual(resource.type, "Texture2D")
        self.assertEqual(resource.path, "res://assets/icon.svg")
        self.assertEqual(resource.id, "Texture2D_assets_icon_svg")

    def test_typed_external_resource_helpers(self) -> None:
        scene = normalize_scene(
            Scene(
                path="res://scenes/main.tscn",
                root=Node2D(
                    "Main",
                    sound=audio_stream("res://assets/tone.wav"),
                    display_font=font("res://assets/display_font.tres"),
                    icon=texture("res://assets/icon.svg"),
                    next_scene=packed_scene("res://scenes/menu.tscn"),
                ),
            )
        )

        self.assertEqual(
            [(resource.type, resource.path, resource.id) for resource in scene.external_resources],
            [
                ("AudioStream", "res://assets/tone.wav", "AudioStream_assets_tone_wav"),
                ("Font", "res://assets/display_font.tres", "Font_assets_display_font_tres"),
                ("PackedScene", "res://scenes/menu.tscn", "PackedScene_scenes_menu_tscn"),
                ("Texture2D", "res://assets/icon.svg", "Texture2D_assets_icon_svg"),
            ],
        )

    def test_rectangle_shape_property_becomes_sub_resource(self) -> None:
        scene = normalize_scene(
            Scene(
                path="res://scenes/main.tscn",
                root=Node2D(
                    "Main",
                    children=[
                        CollisionShape2D(
                            "Hitbox",
                            shape=rectangle_shape_2d(size=Vec2(24, 32)),
                        )
                    ],
                ),
            )
        )

        self.assertEqual(len(scene.sub_resources), 1)
        resource = scene.sub_resources[0]
        self.assertEqual(resource.type, "RectangleShape2D")
        self.assertEqual(resource.id, "RectangleShape2D_rectangle_24_32")
        self.assertEqual(resource.props, {"size": Vec2(24, 32)})
        self.assertEqual(scene.root.children[0].props["shape"].resource_id, resource.id)

    def test_external_resources_dedupe_by_type_and_path(self) -> None:
        scene = normalize_scene(
            Scene(
                path="res://scenes/main.tscn",
                root=Node(
                    name="Main",
                    type="Node",
                    props={
                        "first": texture("res://assets/icon.svg"),
                        "second": texture("res://assets/icon.svg"),
                        "same_path_other_type": ext_resource(
                            "res://assets/icon.svg",
                            type="CompressedTexture2D",
                        ),
                    },
                ),
            )
        )

        self.assertEqual(
            [(resource.type, resource.path, resource.id) for resource in scene.external_resources],
            [
                (
                    "CompressedTexture2D",
                    "res://assets/icon.svg",
                    "CompressedTexture2D_assets_icon_svg",
                ),
                ("Texture2D", "res://assets/icon.svg", "Texture2D_assets_icon_svg"),
            ],
        )
