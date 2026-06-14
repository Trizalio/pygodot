from __future__ import annotations

import json
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pygodot import (
    AnimationPlayer,
    Area2D,
    AudioStreamPlayer,
    Button,
    Color,
    ColorRect,
    CollisionShape2D,
    Game,
    Label,
    Node2D,
    NodePath,
    Node,
    InputAction,
    packed_scene,
    Rect2,
    RectangleShape2D,
    Scene,
    Script,
    Sprite2D,
    Timer,
    Vec2,
    Vec3,
    WindowSettings,
    audio_stream,
    animation,
    ext_resource,
    font,
    key,
    rectangle_shape_2d,
    signal,
    node,
    scene_instance,
    texture,
    value_track,
)
from pygodot.emitters.gdscript import GdScriptEmitter
from pygodot.emitters.project import ProjectEmitter
from pygodot.emitters.tscn import TscnEmitter
from pygodot.emitters.values import gd_value
from pygodot.errors import BuildError, ValidationError
from pygodot.godot_cli import check_project_run
from pygodot.ir.model import IRInputAction, IRProject, IRWindowSettings
from pygodot.ir.normalize import normalize_project, normalize_scene
from pygodot.ir.validate import validate_project, validate_scene


SNAPSHOTS_DIR = Path(__file__).parent / "snapshots"


def make_scene() -> Scene:
    script = Script(
        path="res://scripts/main.gd",
        extends="Node2D",
        body="""
        var counter := 0

        func _on_start_pressed() -> void:
            counter += 1
        """,
    )
    return Scene(
        path="res://scenes/main.tscn",
        root=Node2D(
            "Main",
            script=script,
            children=[
                Label("Title", text="Generated scene", position=(80, 60)),
                Button(
                    "StartButton",
                    text="Click me",
                    position=Vec2(80, 120),
                    signals=[signal("pressed", target=".", method="_on_start_pressed")],
                ),
            ],
        ),
    )


class DslNodeTests(unittest.TestCase):
    def test_animation_player_constructor_creates_animation_player_node(self) -> None:
        pulse = animation(
            "pulse",
            length=1.0,
            loop=True,
            tracks=[
                value_track(
                    "Target:scale",
                    keys=[
                        key(0.0, Vec2(1, 1)),
                        key(1.0, Vec2(2, 2)),
                    ],
                )
            ],
        )
        player = AnimationPlayer("Animator", autoplay="pulse", animations=[pulse])

        self.assertEqual(player.name, "Animator")
        self.assertEqual(player.type, "AnimationPlayer")
        self.assertEqual(player.props, {"autoplay": "pulse"})
        self.assertEqual(player.animations, [pulse])

    def test_audio_stream_player_constructor_creates_audio_node(self) -> None:
        player = AudioStreamPlayer(
            "Player",
            stream=audio_stream("res://assets/tone.wav"),
            volume_db=-8,
        )

        self.assertEqual(player.name, "Player")
        self.assertEqual(player.type, "AudioStreamPlayer")
        self.assertEqual(
            player.props,
            {
                "stream": audio_stream("res://assets/tone.wav"),
                "volume_db": -8,
            },
        )

    def test_area_and_collision_shape_constructors_create_physics_nodes(self) -> None:
        shape = rectangle_shape_2d(size=Vec2(32, 48))
        collision = CollisionShape2D("Hitbox", shape=shape)
        area = Area2D(
            "Trigger",
            position=Vec2(10, 20),
            signals=[signal("area_entered", target=".", method="_on_area_entered")],
            children=[collision],
        )

        self.assertEqual(shape, RectangleShape2D(size=Vec2(32, 48)))
        self.assertEqual(collision.name, "Hitbox")
        self.assertEqual(collision.type, "CollisionShape2D")
        self.assertEqual(collision.props, {"shape": shape})
        self.assertEqual(area.name, "Trigger")
        self.assertEqual(area.type, "Area2D")
        self.assertEqual(area.props, {"position": Vec2(10, 20)})
        self.assertEqual(area.signals[0].signal, "area_entered")
        self.assertEqual(area.children, [collision])

    def test_node_helper_creates_generic_node(self) -> None:
        script = Script(
            path="res://scripts/panel.gd",
            extends="Control",
            body="func _ready() -> void:\n    pass",
        )
        signals = [signal("pressed", target=".", method="_on_pressed")]
        child = Label("Title", text="Hello")

        generic = node(
            "Panel",
            "Control",
            children=[child],
            script=script,
            signals=signals,
            position=Vec2(12, 24),
            visible=True,
        )

        self.assertEqual(generic.name, "Panel")
        self.assertEqual(generic.type, "Control")
        self.assertEqual(generic.props, {"position": Vec2(12, 24), "visible": True})
        self.assertEqual(generic.children, [child])
        self.assertIs(generic.script, script)
        self.assertEqual(generic.signals, signals)

    def test_color_rect_constructor_creates_color_rect_node(self) -> None:
        rect = ColorRect(
            "Panel",
            position=Vec2(10, 20),
            size=Vec2(200, 80),
            color=Color(0.1, 0.2, 0.3),
        )

        self.assertEqual(rect.name, "Panel")
        self.assertEqual(rect.type, "ColorRect")
        self.assertEqual(
            rect.props,
            {
                "position": Vec2(10, 20),
                "size": Vec2(200, 80),
                "color": Color(0.1, 0.2, 0.3),
            },
        )

    def test_sprite2d_constructor_creates_sprite_node(self) -> None:
        sprite = Sprite2D(
            "Logo",
            texture=texture("res://assets/logo.svg"),
            position=Vec2(100, 120),
        )

        self.assertEqual(sprite.name, "Logo")
        self.assertEqual(sprite.type, "Sprite2D")
        self.assertEqual(
            sprite.props,
            {
                "texture": texture("res://assets/logo.svg"),
                "position": Vec2(100, 120),
            },
        )

    def test_scene_instance_constructor_creates_instance_node(self) -> None:
        resource = packed_scene("res://scenes/gem.tscn")
        instance = scene_instance("GemA", resource, position=Vec2(220, 190))

        self.assertEqual(instance.name, "GemA")
        self.assertEqual(instance.type, "")
        self.assertIs(instance.instance, resource)
        self.assertEqual(instance.props, {"position": Vec2(220, 190)})

    def test_scene_instance_requires_packed_scene_resource(self) -> None:
        with self.assertRaisesRegex(ValueError, "PackedScene"):
            scene_instance("Logo", texture("res://assets/logo.svg"))

    def test_timer_constructor_creates_timer_node(self) -> None:
        timer = Timer(
            "PulseTimer",
            wait_time=0.5,
            autostart=True,
            signals=[signal("timeout", target=".", method="_on_timeout")],
        )

        self.assertEqual(timer.name, "PulseTimer")
        self.assertEqual(timer.type, "Timer")
        self.assertEqual(timer.props, {"wait_time": 0.5, "autostart": True})
        self.assertEqual(timer.signals[0].signal, "timeout")

    def test_script_from_file_declares_generated_source(self) -> None:
        script = Script.from_file(
            source="scripts/player.gd",
            path="res://scripts/player.gd",
            extends="Node2D",
        )

        self.assertEqual(script.source, "scripts/player.gd")
        self.assertEqual(script.path, "res://scripts/player.gd")
        self.assertEqual(script.extends, "Node2D")
        self.assertEqual(script.body, "")
        self.assertTrue(script.generated)


class ValueSerializationTests(unittest.TestCase):
    def test_serializes_common_godot_values(self) -> None:
        self.assertEqual(gd_value("hello"), '"hello"')
        self.assertEqual(gd_value(True), "true")
        self.assertEqual(gd_value(None), "null")
        self.assertEqual(gd_value((1, 2)), "Vector2(1, 2)")
        self.assertEqual(gd_value((1, 2, 3)), "Vector3(1, 2, 3)")
        self.assertEqual(gd_value(Vec2(80, 120)), "Vector2(80, 120)")
        self.assertEqual(gd_value(Vec3(1, 2, 3)), "Vector3(1, 2, 3)")
        self.assertEqual(gd_value(Rect2(1, 2, 30, 40)), "Rect2(1, 2, 30, 40)")
        self.assertEqual(gd_value(Color(1, 0.5, 0.25)), "Color(1, 0.5, 0.25, 1.0)")
        self.assertEqual(gd_value(NodePath("../Player")), 'NodePath("../Player")')


class EmitterSnapshotTests(unittest.TestCase):
    def test_project_emitter_snapshot(self) -> None:
        project = IRProject(name="GeneratedGame", main_scene="res://scenes/main.tscn")

        self.assertEqual(
            ProjectEmitter().emit(project),
            """; Generated by pygodot.

config_version=5

[application]

config/name="GeneratedGame"
run/main_scene="res://scenes/main.tscn"
""",
        )

    def test_project_emitter_snapshot_with_input_actions(self) -> None:
        project = IRProject(
            name="GeneratedGame",
            main_scene="res://scenes/main.tscn",
            input_actions=(
                IRInputAction(name="jump", keys=("SPACE",)),
                IRInputAction(name="move_up", keys=("W", "UP")),
            ),
        )

        self.assertEqual(
            ProjectEmitter().emit(project),
            """; Generated by pygodot.

config_version=5

[application]

config/name="GeneratedGame"
run/main_scene="res://scenes/main.tscn"

[input]

jump={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":32,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)]
}
move_up={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":87,"physical_keycode":0,"key_label":0,"unicode":87,"location":0,"echo":false,"script":null), Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":4194320,"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)]
}
""",
        )

    def test_project_emitter_snapshot_with_window_settings(self) -> None:
        project = IRProject(
            name="GeneratedGame",
            main_scene="res://scenes/main.tscn",
            window=IRWindowSettings(width=800, height=600),
        )

        self.assertEqual(
            ProjectEmitter().emit(project),
            """; Generated by pygodot.

config_version=5

[application]

config/name="GeneratedGame"
run/main_scene="res://scenes/main.tscn"

[display]

window/size/viewport_width=800
window/size/viewport_height=600
""",
        )

    def test_gdscript_emitter_snapshot(self) -> None:
        script = normalize_scene(make_scene()).root.script
        assert script is not None

        self.assertEqual(
            GdScriptEmitter().emit(script),
            """extends Node2D

var counter := 0

func _on_start_pressed() -> void:
    counter += 1
""",
        )

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

    def test_minimal_scene_file_snapshot(self) -> None:
        scene = normalize_scene(
            Scene(
                path="res://scenes/minimal.tscn",
                root=Node2D(
                    "Main",
                    children=[
                        Label("Title", text="Hello snapshots"),
                    ],
                ),
            )
        )

        self.assert_matches_snapshot(
            "minimal_scene.tscn",
            TscnEmitter().emit(scene),
        )

    def test_pong_scene_file_snapshot(self) -> None:
        pong = _load_example_game("pong")
        scene = normalize_scene(_find_scene(pong.game, "res://scenes/pong.tscn"))

        self.assert_matches_snapshot(
            "pong_scene.tscn",
            TscnEmitter().emit(scene),
        )

    def test_pong_menu_scene_file_snapshot(self) -> None:
        pong = _load_example_game("pong")
        scene = normalize_scene(_find_scene(pong.game, "res://scenes/menu.tscn"))

        self.assert_matches_snapshot(
            "pong_menu_scene.tscn",
            TscnEmitter().emit(scene),
        )

    def test_pong_script_file_snapshot(self) -> None:
        pong = _load_example_game("pong")

        self.assert_matches_snapshot(
            "pong_script.gd",
            _build_example_script(pong.game, "scripts/pong.gd"),
        )

    def test_snake_scene_file_snapshot(self) -> None:
        snake = _load_example_game("snake")
        scene = normalize_scene(snake.game.scenes[0])

        self.assert_matches_snapshot(
            "snake_scene.tscn",
            TscnEmitter().emit(scene),
        )

    def test_snake_script_file_snapshot(self) -> None:
        snake = _load_example_game("snake")

        self.assert_matches_snapshot(
            "snake_script.gd",
            _build_example_script(snake.game, "scripts/snake.gd"),
        )

    def test_resources_scene_file_snapshot(self) -> None:
        resources = _load_example_game("resources")
        scene = normalize_scene(resources.game.scenes[0])

        self.assert_matches_snapshot(
            "resources_scene.tscn",
            TscnEmitter().emit(scene),
        )

    def test_instancing_gem_scene_file_snapshot(self) -> None:
        instancing = _load_example_game("instancing")
        scene = _find_scene(instancing.game, "res://scenes/gem.tscn")

        self.assert_matches_snapshot(
            "instancing_gem_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_instancing_main_scene_file_snapshot(self) -> None:
        instancing = _load_example_game("instancing")
        scene = _find_scene(instancing.game, "res://scenes/main.tscn")

        self.assert_matches_snapshot(
            "instancing_main_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_timer_scene_file_snapshot(self) -> None:
        timer = _load_example_game("timer")
        scene = timer.game.scenes[0]

        self.assert_matches_snapshot(
            "timer_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_timer_script_file_snapshot(self) -> None:
        timer = _load_example_game("timer")

        self.assert_matches_snapshot(
            "timer_script.gd",
            _build_example_script(timer.game, "scripts/main.gd"),
        )

    def test_audio_scene_file_snapshot(self) -> None:
        audio = _load_example_game("audio")
        scene = audio.game.scenes[0]

        self.assert_matches_snapshot(
            "audio_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_audio_script_file_snapshot(self) -> None:
        audio = _load_example_game("audio")

        self.assert_matches_snapshot(
            "audio_script.gd",
            _build_example_script(audio.game, "scripts/main.gd"),
        )

    def test_font_scene_file_snapshot(self) -> None:
        font_example = _load_example_game("font")
        scene = font_example.game.scenes[0]

        self.assert_matches_snapshot(
            "font_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_animation_scene_file_snapshot(self) -> None:
        animation_example = _load_example_game("animation")
        scene = animation_example.game.scenes[0]

        self.assert_matches_snapshot(
            "animation_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_physics_scene_file_snapshot(self) -> None:
        physics = _load_example_game("physics")
        scene = physics.game.scenes[0]

        self.assert_matches_snapshot(
            "physics_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_physics_script_file_snapshot(self) -> None:
        physics = _load_example_game("physics")

        self.assert_matches_snapshot(
            "physics_script.gd",
            _build_example_script(physics.game, "scripts/main.gd"),
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

    def assert_matches_snapshot(self, snapshot_name: str, actual: str) -> None:
        expected = (SNAPSHOTS_DIR / snapshot_name).read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

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


class BuildTests(unittest.TestCase):
    def test_game_build_writes_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(make_scene())

            result = game.build()

            self.assertEqual(result.project_dir, build_dir)
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [".pygodot/manifest.json", "project.godot", "scenes/main.tscn", "scripts/main.gd"],
            )
            self.assertTrue((build_dir / "project.godot").exists())
            self.assertTrue((build_dir / "scenes" / "main.tscn").exists())
            self.assertTrue((build_dir / "scripts" / "main.gd").exists())
            self.assertEqual(result.manifest_path, build_dir / ".pygodot" / "manifest.json")

    def test_game_build_output_is_stable_across_repeated_builds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(make_scene())

            game.build()
            first = _read_generated_files(build_dir)
            game.build()
            second = _read_generated_files(build_dir)

            self.assertEqual(second, first)

    def test_game_build_does_not_write_referenced_manual_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manual_script = Path(tmp) / "manual" / "player.gd"
            manual_script.parent.mkdir(parents=True)
            manual_script.write_text("extends Node2D\n", encoding="utf-8")
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
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

            result = game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [".pygodot/manifest.json", "project.godot", "scenes/main.tscn"],
            )
            self.assertEqual(result.generated_scripts, [])
            self.assertFalse((build_dir / "manual" / "player.gd").exists())
            self.assertIn(
                'path="res://manual/player.gd"',
                (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8"),
            )

    def test_game_build_writes_generated_script_from_source_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(tmp) / "source"
            source_script = source_root / "scripts" / "player.gd"
            source_script.parent.mkdir(parents=True)
            source_script.write_text(
                "func _ready() -> void:\n    $Label.text = \"Loaded from file\"\n",
                encoding="utf-8",
            )
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=source_root,
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        script=Script.from_file(
                            source="scripts/player.gd",
                            path="res://scripts/player.gd",
                            extends="Node2D",
                        ),
                    ),
                )
            )

            result = game.build()

            generated_script = build_dir / "scripts" / "player.gd"
            self.assertEqual(result.generated_scripts, [generated_script])
            self.assertEqual(
                generated_script.read_text(encoding="utf-8"),
                """# Generated by pygodot. Do not edit by hand.

extends Node2D

func _ready() -> void:
    $Label.text = "Loaded from file"
""",
            )

    def test_game_build_rejects_missing_generated_script_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        script=Script.from_file(
                            source="scripts/missing.gd",
                            path="res://scripts/main.gd",
                            extends="Node2D",
                        ),
                    ),
                )
            )

            with self.assertRaisesRegex(BuildError, "source file does not exist"):
                game.build()

    def test_game_build_rejects_unsafe_generated_script_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        script=Script.from_file(
                            source="../outside.gd",
                            path="res://scripts/main.gd",
                            extends="Node2D",
                        ),
                    ),
                )
            )

            with self.assertRaisesRegex(BuildError, "cannot leave source root"):
                game.build()

    def test_game_build_copies_existing_external_assets_and_writes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(tmp) / "source"
            build_dir = Path(tmp) / "godot_project"
            asset_path = source_root / "assets" / "icon.svg"
            asset_path.parent.mkdir(parents=True)
            asset_path.write_text("<svg></svg>\n", encoding="utf-8")

            game = Game(
                name="GeneratedGame",
                source_root=source_root,
                build_dir=build_dir,
                main_scene="res://scenes/main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://scenes/main.tscn",
                    root=Node2D(
                        "Main",
                        icon=texture("res://assets/icon.svg"),
                    ),
                )
            )

            result = game.build()

            copied_asset = build_dir / "assets" / "icon.svg"
            self.assertEqual(result.copied_resources, [copied_asset])
            self.assertEqual(copied_asset.read_text(encoding="utf-8"), "<svg></svg>\n")

            manifest_path = build_dir / ".pygodot" / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(result.manifest_path, manifest_path)
            self.assertIn(".pygodot/manifest.json", manifest["generated_files"])
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": True,
                        "id": "Texture2D_assets_icon_svg",
                        "path": "res://assets/icon.svg",
                        "type": "Texture2D",
                    }
                ],
            )

    def test_game_build_rejects_unsafe_res_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game = Game(
                name="GeneratedGame",
                source_root=Path(tmp),
                build_dir=build_dir,
                main_scene="res://../main.tscn",
            )
            game.add_scene(
                Scene(
                    path="res://../main.tscn",
                    root=Node2D("Main"),
                )
            )

            with self.assertRaisesRegex(
                BuildError,
                "Unsafe res:// path cannot leave project root: path='res://../main.tscn'",
            ):
                game.build()

    def test_check_project_run_builds_headless_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "pygodot_check_run.log").write_text(
                "Loading resource: res://scenes/main.tscn\n",
                encoding="utf-8",
            )

            with patch("pygodot.godot_cli.subprocess.run") as run:
                run.return_value = subprocess.CompletedProcess(
                    args=[],
                    returncode=0,
                    stdout="fake godot ok\n",
                    stderr="",
                )

                result = check_project_run(
                    project_dir,
                    godot_bin="godot",
                    scene="res://scenes/main.tscn",
                    frames=3,
                )

            self.assertEqual(result.returncode, 0)
            self.assertIn("--headless", result.command)
            self.assertIn("--scene", result.command)
            self.assertIn("res://scenes/main.tscn", result.command)
            self.assertIn("--quit-after", result.command)
            self.assertIn("3", result.command)
            self.assertIn("fake godot ok", result.stdout)
            self.assertIn("Loading resource", result.log_text)

    def test_pong_example_builds_menu_and_game_scenes(self) -> None:
        pong = _load_example_game("pong")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            pong.game.build_dir = build_dir

            result = pong.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/menu.tscn",
                    "scenes/pong.tscn",
                    "scripts/menu.gd",
                    "scripts/pong.gd",
                ],
            )

            menu_scene_text = (build_dir / "scenes" / "menu.tscn").read_text(encoding="utf-8")
            menu_script_text = (build_dir / "scripts" / "menu.gd").read_text(encoding="utf-8")
            scene_text = (build_dir / "scenes" / "pong.tscn").read_text(encoding="utf-8")
            script_text = (build_dir / "scripts" / "pong.gd").read_text(encoding="utf-8")

            self.assertIn('[node name="Menu" type="Control"]', menu_scene_text)
            self.assertIn('[node name="StartButton" type="Button" parent="."]', menu_scene_text)
            self.assertIn(
                '[connection signal="pressed" from="StartButton" to="." method="_on_start_pressed"]',
                menu_scene_text,
            )
            self.assertIn('change_scene_to_file("res://scenes/pong.tscn")', menu_script_text)
            self.assertIn("get_tree().quit()", menu_script_text)

            self.assertIn('[node name="Main" type="Node2D"]', scene_text)
            self.assertIn('[node name="Ball" type="ColorRect" parent="."]', scene_text)
            self.assertIn('[node name="HelpText" type="Label" parent="."]', scene_text)
            self.assertIn("func _process(delta: float) -> void:", script_text)
            self.assertIn('Input.is_action_pressed("left_up")', script_text)
            self.assertIn('Input.is_action_just_pressed("restart")', script_text)
            self.assertIn("func reset_ball(direction: int) -> void:", script_text)

            project_text = (build_dir / "project.godot").read_text(encoding="utf-8")
            self.assertIn('run/main_scene="res://scenes/menu.tscn"', project_text)
            self.assertIn("[display]", project_text)
            self.assertIn("window/size/viewport_width=800", project_text)
            self.assertIn("window/size/viewport_height=600", project_text)
            self.assertIn("[input]", project_text)
            self.assertIn("left_up={", project_text)
            self.assertIn('"keycode":87', project_text)
            self.assertIn("right_down={", project_text)
            self.assertIn('"keycode":4194322', project_text)

    def test_snake_example_builds_draw_based_scene(self) -> None:
        snake = _load_example_game("snake")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            snake.game.build_dir = build_dir

            result = snake.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [".pygodot/manifest.json", "project.godot", "scenes/snake.tscn", "scripts/snake.gd"],
            )

            scene_text = (build_dir / "scenes" / "snake.tscn").read_text(encoding="utf-8")
            script_text = (build_dir / "scripts" / "snake.gd").read_text(encoding="utf-8")
            project_text = (build_dir / "project.godot").read_text(encoding="utf-8")

            self.assertIn('[node name="Snake" type="Node2D"]', scene_text)
            self.assertIn("func _draw() -> void:", script_text)
            self.assertIn('Input.is_action_just_pressed("move_up")', script_text)
            self.assertIn("draw_cell(food", script_text)
            self.assertIn('run/main_scene="res://scenes/snake.tscn"', project_text)
            self.assertIn("window/size/viewport_width=672", project_text)
            self.assertIn("window/size/viewport_height=560", project_text)
            self.assertIn("move_left={", project_text)
            self.assertIn('"keycode":65', project_text)

    def test_resources_example_builds_scene_and_copies_texture(self) -> None:
        resources = _load_example_game("resources")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            resources.game.build_dir = build_dir

            result = resources.game.build()

            copied_asset = build_dir / "assets" / "pygodot_mark.svg"
            self.assertEqual(result.copied_resources, [copied_asset])
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/resources.tscn",
                ],
            )
            self.assertTrue(copied_asset.exists())

            scene_text = (build_dir / "scenes" / "resources.tscn").read_text(encoding="utf-8")
            self.assertIn('[node name="Logo" type="Sprite2D" parent="."]', scene_text)
            self.assertIn('path="res://assets/pygodot_mark.svg"', scene_text)
            self.assertIn('texture = ExtResource("Texture2D_assets_pygodot_mark_svg")', scene_text)

            manifest = json.loads((build_dir / ".pygodot" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": True,
                        "id": "Texture2D_assets_pygodot_mark_svg",
                        "path": "res://assets/pygodot_mark.svg",
                        "type": "Texture2D",
                    }
                ],
            )

    def test_instancing_example_builds_reusable_scene_instances(self) -> None:
        instancing = _load_example_game("instancing")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            instancing.game.build_dir = build_dir

            result = instancing.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/gem.tscn",
                    "scenes/main.tscn",
                ],
            )

            main_scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            self.assertIn(
                '[ext_resource type="PackedScene" path="res://scenes/gem.tscn" '
                'id="PackedScene_scenes_gem_tscn"]',
                main_scene_text,
            )
            self.assertIn(
                '[node name="GemA" parent="." instance=ExtResource("PackedScene_scenes_gem_tscn")]',
                main_scene_text,
            )
            self.assertIn(
                '[node name="GemB" parent="." instance=ExtResource("PackedScene_scenes_gem_tscn")]',
                main_scene_text,
            )

            manifest = json.loads((build_dir / ".pygodot" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": False,
                        "id": "PackedScene_scenes_gem_tscn",
                        "path": "res://scenes/gem.tscn",
                        "type": "PackedScene",
                    }
                ],
            )

    def test_timer_example_builds_signal_connected_timer(self) -> None:
        timer = _load_example_game("timer")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            timer.game.build_dir = build_dir

            result = timer.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/main.tscn",
                    "scripts/main.gd",
                ],
            )

            scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            self.assertIn('[node name="PulseTimer" type="Timer" parent="."]', scene_text)
            self.assertIn("wait_time = 0.5", scene_text)
            self.assertIn("autostart = true", scene_text)
            self.assertIn(
                '[connection signal="timeout" from="PulseTimer" to="." '
                'method="_on_pulse_timer_timeout"]',
                scene_text,
            )

    def test_audio_example_builds_player_and_copies_stream(self) -> None:
        audio = _load_example_game("audio")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            audio.game.build_dir = build_dir

            result = audio.game.build()

            copied_asset = build_dir / "assets" / "tone.wav"
            self.assertEqual(result.copied_resources, [copied_asset])
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/main.tscn",
                    "scripts/main.gd",
                ],
            )
            self.assertTrue(copied_asset.exists())

            scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            self.assertIn('[node name="Player" type="AudioStreamPlayer" parent="."]', scene_text)
            self.assertIn('path="res://assets/tone.wav"', scene_text)
            self.assertIn('stream = ExtResource("AudioStream_assets_tone_wav")', scene_text)
            self.assertIn(
                '[connection signal="pressed" from="PlayButton" to="." method="_on_play_button_pressed"]',
                scene_text,
            )
            self.assertIn(
                '[connection signal="finished" from="Player" to="." method="_on_player_finished"]',
                scene_text,
            )

            manifest = json.loads((build_dir / ".pygodot" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": True,
                        "id": "AudioStream_assets_tone_wav",
                        "path": "res://assets/tone.wav",
                        "type": "AudioStream",
                    },
                    {
                        "copied": False,
                        "id": "Script_scripts_main_gd",
                        "path": "res://scripts/main.gd",
                        "type": "Script",
                    },
                ],
            )

    def test_font_example_builds_label_and_copies_font_resource(self) -> None:
        font_example = _load_example_game("font")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            font_example.game.build_dir = build_dir

            result = font_example.game.build()

            copied_ttf = build_dir / "assets" / "WDXL_Lubrifont_TC" / "WDXLLubrifontTC-Regular.ttf"
            copied_tres = build_dir / "assets" / "display_font.tres"
            self.assertEqual(result.copied_resources, [copied_ttf, copied_tres])
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [".pygodot/manifest.json", "project.godot", "scenes/main.tscn"],
            )
            self.assertTrue(copied_ttf.exists())
            self.assertTrue(copied_tres.exists())

            scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            self.assertIn('[node name="Title" type="Label" parent="."]', scene_text)
            self.assertIn('path="res://assets/display_font.tres"', scene_text)
            self.assertIn('theme_override_fonts/font = ExtResource("Font_assets_display_font_tres")', scene_text)
            self.assertIn("theme_override_font_sizes/font_size = 30", scene_text)
            self.assertIn('[node name="GoogleFontTitle" type="Label" parent="."]', scene_text)
            self.assertIn('path="res://assets/WDXL_Lubrifont_TC/WDXLLubrifontTC-Regular.ttf"', scene_text)
            self.assertIn(
                'theme_override_fonts/font = '
                'ExtResource("Font_assets_WDXL_Lubrifont_TC_WDXLLubrifontTC_Regular_ttf")',
                scene_text,
            )

            manifest = json.loads((build_dir / ".pygodot" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": True,
                        "id": "Font_assets_WDXL_Lubrifont_TC_WDXLLubrifontTC_Regular_ttf",
                        "path": "res://assets/WDXL_Lubrifont_TC/WDXLLubrifontTC-Regular.ttf",
                        "type": "Font",
                    },
                    {
                        "copied": True,
                        "id": "Font_assets_display_font_tres",
                        "path": "res://assets/display_font.tres",
                        "type": "Font",
                    }
                ],
            )

    def test_animation_example_builds_animation_player_subresources(self) -> None:
        animation_example = _load_example_game("animation")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            animation_example.game.build_dir = build_dir

            result = animation_example.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [".pygodot/manifest.json", "project.godot", "scenes/main.tscn"],
            )

            scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            self.assertIn('[sub_resource type="Animation" id="Animation_Animator_pulse"]', scene_text)
            self.assertIn(
                '[sub_resource type="AnimationLibrary" id="AnimationLibrary_Animator"]',
                scene_text,
            )
            self.assertIn('[node name="Animator" type="AnimationPlayer" parent="."]', scene_text)
            self.assertIn('autoplay = "pulse"', scene_text)
            self.assertIn('libraries = {&"": SubResource("AnimationLibrary_Animator")}', scene_text)

    def test_physics_example_builds_collision_shape_subresources(self) -> None:
        physics = _load_example_game("physics")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            physics.game.build_dir = build_dir

            result = physics.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/main.tscn",
                    "scripts/main.gd",
                ],
            )

            scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            self.assertIn(
                '[sub_resource type="RectangleShape2D" id="RectangleShape2D_rectangle_64_64"]',
                scene_text,
            )
            self.assertIn(
                '[sub_resource type="RectangleShape2D" id="RectangleShape2D_rectangle_90_90"]',
                scene_text,
            )
            self.assertIn('[node name="Probe" type="Area2D" parent="."]', scene_text)
            self.assertIn('[node name="ProbeShape" type="CollisionShape2D" parent="Probe"]', scene_text)
            self.assertIn('shape = SubResource("RectangleShape2D_rectangle_64_64")', scene_text)
            self.assertIn(
                '[connection signal="area_entered" from="Probe" to="." method="_on_probe_area_entered"]',
                scene_text,
            )

            script_text = (build_dir / "scripts" / "main.gd").read_text(encoding="utf-8")
            self.assertIn("func _physics_process(delta: float) -> void:", script_text)
            self.assertIn("pygodot_physics_area_entered", script_text)


def _read_generated_files(build_dir: Path) -> dict[str, str]:
    return {
        path.relative_to(build_dir).as_posix(): path.read_text(encoding="utf-8")
        for path in sorted(build_dir.rglob("*"))
        if path.is_file()
    }


def _load_example_game(name: str):
    path = Path(__file__).parents[1] / "examples" / name / "game.py"
    spec = importlib.util.spec_from_file_location(f"pygodot_example_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load example module from {path}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _find_scene(game: Game, path: str) -> Scene:
    for scene in game.scenes:
        if scene.path == path:
            return scene
    raise AssertionError(f"Missing scene: {path}")


def _build_example_script(game: Game, relative_path: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        build_dir = Path(tmp) / "godot_project"
        game.build_dir = build_dir
        game.build()
        return (build_dir / relative_path).read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
