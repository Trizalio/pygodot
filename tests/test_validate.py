from __future__ import annotations

import unittest
from pathlib import Path

from pygodot import (
    Game,
    InputAction,
    Label,
    Node,
    Node2D,
    Scene,
    Script,
    Vec2,
    WindowSettings,
    texture,
)
from pygodot.errors import ValidationError
from pygodot.ir.model import IRGeneratedResource, IRNode, IRProject, IRScene, IRSubResource
from pygodot.ir.normalize import normalize_project, normalize_scene
from pygodot.ir.validate import validate_project, validate_scene
from tests.helpers import make_scene


class ValidationTests(unittest.TestCase):
    def test_duplicate_sibling_node_names_are_rejected(self) -> None:
        scene = Scene(
            path="res://scenes/main.tscn",
            root=Node2D(
                "Main",
                children=[
                    Label("Title", text="One"),
                    Label("Title", text="Two"),
                ],
            ),
        )

        with self.assertRaisesRegex(ValidationError, "Duplicate child node name"):
            validate_scene(normalize_scene(scene))

    def test_generated_script_body_must_not_be_empty(self) -> None:
        scene = Scene(
            path="res://scenes/main.tscn",
            root=Node2D(
                "Main",
                script=Script(path="res://scripts/main.gd", extends="Node2D"),
            ),
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Generated script body must not be empty: scene='res://scenes/main.tscn', "
            "node='.', script_path='res://scripts/main.gd'",
        ):
            validate_scene(normalize_scene(scene))

    def test_unsupported_property_value_error_includes_context(self) -> None:
        scene = Scene(
            path="res://scenes/main.tscn",
            root=Node2D(
                "Main",
                metadata=object(),
            ),
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Unsupported value for property 'metadata': scene='res://scenes/main.tscn', "
            "node='.', value=.*value_type=object",
        ):
            validate_scene(normalize_scene(scene))

    def test_main_scene_error_includes_registered_scenes(self) -> None:
        game = Game(
            name="GeneratedGame",
            source_root=Path("."),
            build_dir=Path("build/godot_project"),
            main_scene="res://missing.tscn",
        )
        game.add_scene(make_scene())

        with self.assertRaisesRegex(
            ValidationError,
            "main_scene='res://missing.tscn'.*registered_scenes=\\['res://scenes/main.tscn'\\]",
        ):
            game.build()

    def test_input_action_names_are_validated(self) -> None:
        project = normalize_project(
            name="GeneratedGame",
            main_scene="res://scenes/main.tscn",
            scenes=[make_scene()],
            input_actions=[InputAction("move-up", ("W",))],
        )

        with self.assertRaisesRegex(ValidationError, "Input action name"):
            validate_project(project)

    def test_input_action_keys_are_validated(self) -> None:
        project = normalize_project(
            name="GeneratedGame",
            main_scene="res://scenes/main.tscn",
            scenes=[make_scene()],
            input_actions=[InputAction("move_up", ("NOT_A_KEY",))],
        )

        with self.assertRaisesRegex(ValidationError, "Unsupported input action key"):
            validate_project(project)

    def test_input_action_mouse_buttons_are_validated(self) -> None:
        project = normalize_project(
            name="GeneratedGame",
            main_scene="res://scenes/main.tscn",
            scenes=[make_scene()],
            input_actions=[InputAction("shoot", (), ("SIDEWAYS",))],
        )

        with self.assertRaisesRegex(ValidationError, "Unsupported input action mouse button"):
            validate_project(project)

    def test_input_action_allows_mouse_button_without_key(self) -> None:
        project = normalize_project(
            name="GeneratedGame",
            main_scene="res://scenes/main.tscn",
            scenes=[make_scene()],
            input_actions=[InputAction("shoot", (), ("LEFT",))],
        )

        validate_project(project)

    def test_duplicate_input_actions_are_rejected(self) -> None:
        project = normalize_project(
            name="GeneratedGame",
            main_scene="res://scenes/main.tscn",
            scenes=[make_scene()],
            input_actions=[
                InputAction("jump", ("SPACE",)),
                InputAction("jump", ("W",)),
            ],
        )

        with self.assertRaisesRegex(ValidationError, "Duplicate input action name"):
            validate_project(project)

    def test_window_size_is_validated(self) -> None:
        project = normalize_project(
            name="GeneratedGame",
            main_scene="res://scenes/main.tscn",
            scenes=[make_scene()],
            window=WindowSettings(size=Vec2(0, 600)),
        )

        with self.assertRaisesRegex(ValidationError, "Window size must be positive"):
            validate_project(project)

    def test_generated_script_cannot_define_body_and_source(self) -> None:
        scene = Scene(
            path="res://scenes/main.tscn",
            root=Node2D(
                "Main",
                script=Script(
                    path="res://scripts/main.gd",
                    extends="Node2D",
                    body="func _ready() -> void:\n    pass",
                    source="scripts/main.gd",
                ),
            ),
        )

        with self.assertRaisesRegex(ValidationError, "either body or source"):
            validate_scene(normalize_scene(scene))

    def test_sub_resource_props_are_validated(self) -> None:
        scene = IRScene(
            path="res://scenes/main.tscn",
            root=IRNode(name="Main", type="Node2D", path=".", parent_path=None),
            sub_resources=(
                IRSubResource(
                    type="RectangleShape2D",
                    id="RectangleShape2D_bad",
                    props={"metadata": object()},
                ),
            ),
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Unsupported value for sub-resource 'RectangleShape2D_bad' property 'metadata'",
        ):
            validate_scene(scene)

    def test_unsupported_generated_resource_type_is_rejected(self) -> None:
        project = IRProject(
            name="GeneratedGame",
            main_scene="res://scenes/main.tscn",
            scenes=(normalize_scene(make_scene()),),
            generated_resources=(
                IRGeneratedResource(
                    type="GradientTexture2D",
                    path="res://ui/gradient.tres",
                    id="GradientTexture2D_ui_gradient_tres",
                ),
            ),
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Unsupported generated resource type: resource_path='res://ui/gradient.tres'",
        ):
            validate_project(project)
