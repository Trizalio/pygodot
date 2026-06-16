from __future__ import annotations

import unittest

from pygodot import (
    Autoload,
    CollisionShape2D,
    Color,
    InputAction,
    Node,
    Node2D,
    ProjectSetting,
    Scene,
    Vec2,
    audio_stream,
    circle_shape_2d,
    ext_resource,
    font,
    label_settings,
    packed_scene,
    rectangle_shape_2d,
    style_box_flat,
    sub_resource,
    texture,
)
from pygodot.ir.model import IRExternalResourceRef
from pygodot.ir.normalize import normalize_project, normalize_scene


class NormalizeTests(unittest.TestCase):
    def test_normalize_project_autoloads_icon_and_extra_settings(self) -> None:
        project = normalize_project(
            name="GeneratedGame",
            main_scene="res://scenes/main.tscn",
            scenes=[
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D("Main"),
                )
            ],
            autoloads=[Autoload("GameState", "res://scripts/game_state.gd")],
            icon="res://resources/icon.png",
            project_settings=[ProjectSetting("audio/output_latency/web", 200)],
        )

        self.assertEqual(len(project.autoloads), 1)
        self.assertEqual(project.autoloads[0].name, "GameState")
        self.assertEqual(project.autoloads[0].path, "res://scripts/game_state.gd")
        self.assertEqual(project.autoloads[0].resource_id, "Script_scripts_game_state_gd")
        self.assertIsNotNone(project.icon)
        self.assertEqual(project.icon.path, "res://resources/icon.png")
        self.assertEqual(project.icon.id, "Texture2D_resources_icon_png")
        self.assertEqual(project.project_settings[0].path, "audio/output_latency/web")
        self.assertEqual(project.project_settings[0].value, 200)

    def test_normalize_input_action_mouse_buttons(self) -> None:
        project = normalize_project(
            name="GeneratedGame",
            main_scene="res://scenes/main.tscn",
            scenes=[
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D("Main"),
                )
            ],
            input_actions=[InputAction("shoot", ("SPACE",), ("left", "wheel-down"))],
        )

        self.assertEqual(project.input_actions[0].keys, ("SPACE",))
        self.assertEqual(project.input_actions[0].mouse_buttons, ("LEFT", "WHEEL_DOWN"))

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

    def test_generic_sub_resource_property_becomes_sub_resource(self) -> None:
        scene = normalize_scene(
            Scene(
                path="res://scenes/main.tscn",
                root=Node2D(
                    "Main",
                    children=[
                        CollisionShape2D(
                            "Hitbox",
                            shape=sub_resource(
                                "RectangleShape2D",
                                id_hint="player_hitbox",
                                size=Vec2(24, 32),
                            ),
                        )
                    ],
                ),
            )
        )

        self.assertEqual(len(scene.sub_resources), 1)
        resource = scene.sub_resources[0]
        self.assertEqual(resource.type, "RectangleShape2D")
        self.assertEqual(resource.id, "RectangleShape2D_player_hitbox")
        self.assertEqual(resource.props, {"size": Vec2(24, 32)})
        self.assertEqual(scene.root.children[0].props["shape"].resource_id, resource.id)

    def test_circle_shape_property_becomes_sub_resource(self) -> None:
        scene = normalize_scene(
            Scene(
                path="res://scenes/main.tscn",
                root=Node2D(
                    "Main",
                    children=[
                        CollisionShape2D(
                            "Hitbox",
                            shape=circle_shape_2d(radius=12),
                        )
                    ],
                ),
            )
        )

        self.assertEqual(len(scene.sub_resources), 1)
        resource = scene.sub_resources[0]
        self.assertEqual(resource.type, "CircleShape2D")
        self.assertEqual(resource.id, "CircleShape2D_circle_12")
        self.assertEqual(resource.props, {"radius": 12})
        self.assertEqual(scene.root.children[0].props["shape"].resource_id, resource.id)

    def test_sub_resources_dedupe_by_type_and_id_hint(self) -> None:
        scene = normalize_scene(
            Scene(
                path="res://scenes/main.tscn",
                root=Node2D(
                    "Main",
                    children=[
                        CollisionShape2D(
                            "First",
                            shape=circle_shape_2d(radius=12),
                        ),
                        CollisionShape2D(
                            "Second",
                            shape=circle_shape_2d(radius=12),
                        ),
                    ],
                ),
            )
        )

        self.assertEqual(len(scene.sub_resources), 1)
        resource_id = scene.sub_resources[0].id
        self.assertEqual(resource_id, "CircleShape2D_circle_12")
        self.assertEqual(scene.root.children[0].props["shape"].resource_id, resource_id)
        self.assertEqual(scene.root.children[1].props["shape"].resource_id, resource_id)

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

    def test_generated_label_settings_becomes_external_ref_and_project_resource(self) -> None:
        project = normalize_project(
            name="GeneratedResources",
            main_scene="res://scenes/main.tscn",
            scenes=[
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        label_settings=label_settings(
                            "res://ui/title_label_settings.tres",
                            font=font("res://assets/display.ttf"),
                            font_size=32,
                            font_color=Color(1, 1, 1),
                        ),
                    ),
                )
            ],
        )

        self.assertEqual(
            [(resource.type, resource.path, resource.id) for resource in project.scenes[0].external_resources],
            [
                (
                    "LabelSettings",
                    "res://ui/title_label_settings.tres",
                    "LabelSettings_ui_title_label_settings_tres",
                )
            ],
        )
        self.assertEqual(len(project.generated_resources), 1)
        resource = project.generated_resources[0]
        self.assertEqual(resource.type, "LabelSettings")
        self.assertEqual(resource.path, "res://ui/title_label_settings.tres")
        self.assertEqual(resource.id, "LabelSettings_ui_title_label_settings_tres")
        self.assertEqual(
            resource.props,
            {
                "font": IRExternalResourceRef("Font_assets_display_ttf"),
                "font_size": 32,
                "font_color": Color(1, 1, 1),
            },
        )
        self.assertEqual(
            [(item.type, item.path, item.id) for item in resource.external_resources],
            [("Font", "res://assets/display.ttf", "Font_assets_display_ttf")],
        )

    def test_generated_style_box_flat_becomes_external_ref_and_project_resource(self) -> None:
        project = normalize_project(
            name="GeneratedResources",
            main_scene="res://scenes/main.tscn",
            scenes=[
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node(
                        name="Panel",
                        type="Panel",
                        props={
                            "theme_override_styles": {
                                "panel": style_box_flat(
                                    "res://ui/panel_style.tres",
                                    bg_color=Color(0.1, 0.2, 0.3),
                                    border_width_all=2,
                                )
                            }
                        },
                    ),
                )
            ],
        )

        self.assertEqual(
            [(resource.type, resource.path, resource.id) for resource in project.scenes[0].external_resources],
            [
                (
                    "StyleBoxFlat",
                    "res://ui/panel_style.tres",
                    "StyleBoxFlat_ui_panel_style_tres",
                )
            ],
        )
        self.assertEqual(len(project.generated_resources), 1)
        resource = project.generated_resources[0]
        self.assertEqual(resource.type, "StyleBoxFlat")
        self.assertEqual(resource.path, "res://ui/panel_style.tres")
        self.assertEqual(resource.id, "StyleBoxFlat_ui_panel_style_tres")
        self.assertEqual(
            resource.props,
            {
                "bg_color": Color(0.1, 0.2, 0.3),
                "border_width_bottom": 2,
                "border_width_left": 2,
                "border_width_right": 2,
                "border_width_top": 2,
            },
        )
