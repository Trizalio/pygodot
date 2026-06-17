from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pygodot import Label, Node2D, Scene
from pygodot.emitters.project import ProjectEmitter
from pygodot.emitters.tscn import TscnEmitter
from pygodot.ir.normalize import normalize_project, normalize_scene
from tests.helpers import SnapshotTestCase, _build_example_file, _build_example_script, _find_scene, _load_example_game


class ExampleSnapshotTests(SnapshotTestCase):
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

    def test_template_script_scene_file_snapshot(self) -> None:
        template_script = _load_example_game("template_script")
        scene = template_script.game.scenes[0]

        self.assert_matches_snapshot(
            "template_script_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_template_script_file_snapshot(self) -> None:
        template_script = _load_example_game("template_script")

        self.assert_matches_snapshot(
            "template_script.gd",
            _build_example_script(template_script.game, "scripts/main.gd"),
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

    def test_flappy_scene_file_snapshot(self) -> None:
        flappy = _load_example_game("flappy")
        scene = flappy.game.scenes[0]

        self.assert_matches_snapshot(
            "flappy_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_flappy_script_file_snapshot(self) -> None:
        flappy = _load_example_game("flappy")

        self.assert_matches_snapshot(
            "flappy_script.gd",
            _build_example_script(flappy.game, "scripts/main.gd"),
        )

    def test_generated_tres_scene_file_snapshot(self) -> None:
        generated_tres = _load_example_game("generated_tres")
        scene = generated_tres.game.scenes[0]

        self.assert_matches_snapshot(
            "generated_tres_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_generated_tres_resource_file_snapshot(self) -> None:
        generated_tres = _load_example_game("generated_tres")

        self.assert_matches_snapshot(
            "generated_tres_title_label_settings.tres",
            _build_example_file(generated_tres.game, "ui/title_label_settings.tres"),
        )

    def test_ui_panel_scene_file_snapshot(self) -> None:
        ui_panel = _load_example_game("ui_panel")
        scene = ui_panel.game.scenes[0]

        self.assert_matches_snapshot(
            "ui_panel_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_ui_panel_title_label_settings_snapshot(self) -> None:
        ui_panel = _load_example_game("ui_panel")

        self.assert_matches_snapshot(
            "ui_panel_title_label_settings.tres",
            _build_example_file(ui_panel.game, "ui/title_label_settings.tres"),
        )

    def test_ui_panel_section_label_settings_snapshot(self) -> None:
        ui_panel = _load_example_game("ui_panel")

        self.assert_matches_snapshot(
            "ui_panel_section_label_settings.tres",
            _build_example_file(ui_panel.game, "ui/section_label_settings.tres"),
        )

    def test_ui_panel_style_box_flat_snapshot(self) -> None:
        ui_panel = _load_example_game("ui_panel")

        self.assert_matches_snapshot(
            "ui_panel_panel_style.tres",
            _build_example_file(ui_panel.game, "ui/panel_style.tres"),
        )

    def test_ld49_ui_shell_scene_file_snapshot(self) -> None:
        ui_shell = _load_example_game("ld49_ui_shell")
        scene = ui_shell.game.scenes[0]

        self.assert_matches_snapshot(
            "ld49_ui_shell_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_ld49_scene_flow_project_snapshot(self) -> None:
        scene_flow = _load_example_game("ld49_scene_flow")

        self.assert_matches_snapshot(
            "ld49_scene_flow_project.godot",
            ProjectEmitter().emit(
                normalize_project(
                    name=scene_flow.game.name,
                    main_scene=scene_flow.game.main_scene,
                    scenes=scene_flow.game.scenes,
                    window=scene_flow.game.window,
                    autoloads=scene_flow.game.autoloads,
                )
            ),
        )

    def test_ld49_scene_flow_main_scene_snapshot(self) -> None:
        scene_flow = _load_example_game("ld49_scene_flow")
        scene = _find_scene(scene_flow.game, "res://scenes/main.tscn")

        self.assert_matches_snapshot(
            "ld49_scene_flow_main_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_ld49_unit_card_main_scene_snapshot(self) -> None:
        unit_card = _load_example_game("ld49_unit_card")
        scene = _find_scene(unit_card.game, "res://scenes/main.tscn")

        self.assert_matches_snapshot(
            "ld49_unit_card_main_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )

    def test_ld49_unit_card_unit_scene_snapshot(self) -> None:
        unit_card = _load_example_game("ld49_unit_card")
        scene = _find_scene(unit_card.game, "res://scenes/unit.tscn")

        self.assert_matches_snapshot(
            "ld49_unit_card_scene.tscn",
            TscnEmitter().emit(normalize_scene(scene)),
        )


class ExampleBuildTests(unittest.TestCase):
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
                        "ownership": "copied",
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
                        "ownership": "generated",
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

    def test_template_script_example_builds_template_script(self) -> None:
        template_script = _load_example_game("template_script")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            template_script.game.build_dir = build_dir

            result = template_script.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [".pygodot/manifest.json", "project.godot", "scenes/main.tscn", "scripts/main.gd"],
            )
            script_text = (build_dir / "scripts" / "main.gd").read_text(encoding="utf-8")
            self.assertIn("const INITIAL_COUNT := 3", script_text)
            self.assertIn('$StatusLabel.text = "Template rendered GDScript (%s)"', script_text)

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
                        "ownership": "copied",
                        "path": "res://assets/tone.wav",
                        "type": "AudioStream",
                    },
                    {
                        "copied": False,
                        "id": "Script_scripts_main_gd",
                        "ownership": "generated",
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
                        "ownership": "copied",
                        "path": "res://assets/WDXL_Lubrifont_TC/WDXLLubrifontTC-Regular.ttf",
                        "type": "Font",
                    },
                    {
                        "copied": True,
                        "id": "Font_assets_display_font_tres",
                        "ownership": "copied",
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

    def test_flappy_example_builds_playable_collision_scene(self) -> None:
        flappy = _load_example_game("flappy")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            flappy.game.build_dir = build_dir

            result = flappy.game.build()

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
            script_text = (build_dir / "scripts" / "main.gd").read_text(encoding="utf-8")
            project_text = (build_dir / "project.godot").read_text(encoding="utf-8")

            self.assertIn('[node name="Bird" type="Area2D" parent="."]', scene_text)
            self.assertIn('[node name="Ground" type="Area2D" parent="."]', scene_text)
            self.assertIn('[node name="PipeTopA" type="Area2D" parent="."]', scene_text)
            self.assertIn('[node name="BirdShape" type="CollisionShape2D" parent="Bird"]', scene_text)
            self.assertIn('[node name="SpawnTimer" type="Timer" parent="."]', scene_text)
            self.assertIn('shape = SubResource("RectangleShape2D_rectangle_34_26")', scene_text)
            self.assertIn(
                '[connection signal="area_entered" from="Bird" to="." method="_on_bird_area_entered"]',
                scene_text,
            )
            self.assertIn(
                '[connection signal="timeout" from="SpawnTimer" to="." method="_on_spawn_timer_timeout"]',
                scene_text,
            )
            self.assertIn("func _physics_process(delta: float) -> void:", script_text)
            self.assertIn('Input.is_action_just_pressed("flap")', script_text)
            self.assertIn('Input.is_action_just_pressed("restart")', script_text)
            self.assertIn("func game_over() -> void:", script_text)
            self.assertIn('[display]', project_text)
            self.assertIn("window/size/viewport_width=480", project_text)
            self.assertIn("window/size/viewport_height=720", project_text)
            self.assertIn("[input]", project_text)
            self.assertIn("flap={", project_text)
            self.assertIn('"keycode":32', project_text)
            self.assertIn('"keycode":4194320', project_text)
            self.assertIn("restart={", project_text)

    def test_mouse_input_example_builds_left_click_action(self) -> None:
        mouse_input = _load_example_game("mouse_input")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            mouse_input.game.build_dir = build_dir

            result = mouse_input.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [".pygodot/manifest.json", "project.godot", "scenes/main.tscn", "scripts/main.gd"],
            )

            scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            script_text = (build_dir / "scripts" / "main.gd").read_text(encoding="utf-8")
            project_text = (build_dir / "project.godot").read_text(encoding="utf-8")

            self.assertIn('[node name="Main" type="Node2D"]', scene_text)
            self.assertIn('[node name="Marker" type="ColorRect" parent="."]', scene_text)
            self.assertIn('[node name="Counter" type="Label" parent="."]', scene_text)
            self.assertIn('Input.is_action_just_pressed("place_marker")', script_text)
            self.assertIn("$Marker.position = get_viewport().get_mouse_position()", script_text)
            self.assertIn("place_marker={", project_text)
            self.assertIn("InputEventMouseButton", project_text)
            self.assertIn('"button_index":1', project_text)

    def test_generated_tres_example_builds_label_settings_resource(self) -> None:
        generated_tres = _load_example_game("generated_tres")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            generated_tres.game.build_dir = build_dir

            result = generated_tres.game.build()

            generated_resource = build_dir / "ui" / "title_label_settings.tres"
            self.assertEqual(result.generated_resources, [generated_resource])
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/main.tscn",
                    "ui/title_label_settings.tres",
                ],
            )
            self.assertTrue(generated_resource.exists())

            scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            resource_text = generated_resource.read_text(encoding="utf-8")
            self.assertIn('label_settings = ExtResource("LabelSettings_ui_title_label_settings_tres")', scene_text)
            self.assertIn('[gd_resource type="LabelSettings" format=3]', resource_text)
            self.assertIn("font_size = 36", resource_text)

            manifest = json.loads((build_dir / ".pygodot" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["generated_resources"], ["ui/title_label_settings.tres"])

    def test_ui_panel_example_builds_static_dashboard(self) -> None:
        ui_panel = _load_example_game("ui_panel")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            ui_panel.game.build_dir = build_dir

            result = ui_panel.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/main.tscn",
                    "ui/panel_style.tres",
                    "ui/section_label_settings.tres",
                    "ui/title_label_settings.tres",
                ],
            )
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.generated_resources),
                ["ui/panel_style.tres", "ui/section_label_settings.tres", "ui/title_label_settings.tres"],
            )
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.copied_resources),
                ["font/assets/WDXL_Lubrifont_TC/WDXLLubrifontTC-Regular.ttf"],
            )

            scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            project_text = (build_dir / "project.godot").read_text(encoding="utf-8")
            self.assertIn('[node name="Dashboard" type="Control"]', scene_text)
            self.assertIn('[node name="StatusPanel" type="Panel" parent="."]', scene_text)
            self.assertIn('theme_override_styles = {"panel": ExtResource("StyleBoxFlat_ui_panel_style_tres")}', scene_text)
            self.assertIn('[node name="PrimaryAction" type="Button" parent="."]', scene_text)
            self.assertIn('label_settings = ExtResource("LabelSettings_ui_title_label_settings_tres")', scene_text)
            self.assertIn('label_settings = ExtResource("LabelSettings_ui_section_label_settings_tres")', scene_text)
            self.assertIn("window/size/viewport_width=720", project_text)
            self.assertIn("window/size/viewport_height=480", project_text)

            manifest = json.loads((build_dir / ".pygodot" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["generated_resources"],
                ["ui/panel_style.tres", "ui/section_label_settings.tres", "ui/title_label_settings.tres"],
            )
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": True,
                        "id": "Font_font_assets_WDXL_Lubrifont_TC_WDXLLubrifontTC_Regular_ttf",
                        "ownership": "copied",
                        "path": "res://font/assets/WDXL_Lubrifont_TC/WDXLLubrifontTC-Regular.ttf",
                        "type": "Font",
                    },
                    {
                        "copied": False,
                        "id": "LabelSettings_ui_section_label_settings_tres",
                        "ownership": "generated",
                        "path": "res://ui/section_label_settings.tres",
                        "type": "LabelSettings",
                    },
                    {
                        "copied": False,
                        "id": "LabelSettings_ui_title_label_settings_tres",
                        "ownership": "generated",
                        "path": "res://ui/title_label_settings.tres",
                        "type": "LabelSettings",
                    },
                    {
                        "copied": False,
                        "id": "StyleBoxFlat_ui_panel_style_tres",
                        "ownership": "generated",
                        "path": "res://ui/panel_style.tres",
                        "type": "StyleBoxFlat",
                    },
                ],
            )

    def test_ld49_ui_shell_example_builds_control_menu(self) -> None:
        ui_shell = _load_example_game("ld49_ui_shell")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            ui_shell.game.build_dir = build_dir

            result = ui_shell.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/main.tscn",
                    "scripts/main.gd",
                ],
            )
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.copied_resources),
                ["assets/banner.svg"],
            )

            scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            script_text = (build_dir / "scripts" / "main.gd").read_text(encoding="utf-8")
            project_text = (build_dir / "project.godot").read_text(encoding="utf-8")

            self.assertIn('[node name="Main" type="MarginContainer" groups=["ld49_ui_shell"]]', scene_text)
            self.assertIn('[node name="Panel" type="Panel" parent="."]', scene_text)
            self.assertIn('[node name="VBox" type="VBoxContainer" parent="Panel"]', scene_text)
            self.assertIn('[node name="MenuCenter" type="CenterContainer" parent="Panel/VBox"]', scene_text)
            self.assertIn('[node name="Banner" type="TextureRect" parent="Panel/VBox"]', scene_text)
            self.assertIn('texture = ExtResource("Texture2D_assets_banner_svg")', scene_text)
            self.assertIn('[node name="BackgroundMusic" type="AudioStreamPlayer" parent="."]', scene_text)
            self.assertIn('binds=["start"]', scene_text)
            self.assertIn('func _on_menu_action(action: String) -> void:', script_text)
            self.assertIn("window/size/viewport_width=540", project_text)
            self.assertIn("window/size/viewport_height=750", project_text)
            self.assertIn('window/stretch/mode="canvas_items"', project_text)
            self.assertIn('window/stretch/aspect="expand"', project_text)

            manifest = json.loads((build_dir / ".pygodot" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": False,
                        "id": "Script_scripts_main_gd",
                        "ownership": "generated",
                        "path": "res://scripts/main.gd",
                        "type": "Script",
                    },
                    {
                        "copied": True,
                        "id": "Texture2D_assets_banner_svg",
                        "ownership": "copied",
                        "path": "res://assets/banner.svg",
                        "type": "Texture2D",
                    },
                ],
            )

    def test_ld49_scene_flow_example_builds_autoload_scene_flow(self) -> None:
        scene_flow = _load_example_game("ld49_scene_flow")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            scene_flow.game.build_dir = build_dir

            result = scene_flow.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/fader.tscn",
                    "scenes/intro.tscn",
                    "scenes/main.tscn",
                    "scripts/fader.gd",
                    "scripts/intro.gd",
                    "scripts/main.gd",
                ],
            )
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.copied_resources),
                ["scripts/audio_manager.gd", "scripts/scene_changer.gd"],
            )

            project_text = (build_dir / "project.godot").read_text(encoding="utf-8")
            main_scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            intro_scene_text = (build_dir / "scenes" / "intro.tscn").read_text(encoding="utf-8")
            fader_scene_text = (build_dir / "scenes" / "fader.tscn").read_text(encoding="utf-8")
            main_script_text = (build_dir / "scripts" / "main.gd").read_text(encoding="utf-8")
            scene_changer_text = (build_dir / "scripts" / "scene_changer.gd").read_text(encoding="utf-8")

            self.assertIn("[autoload]", project_text)
            self.assertIn('SceneChanger="*res://scripts/scene_changer.gd"', project_text)
            self.assertIn('AudioManager="*res://scripts/audio_manager.gd"', project_text)
            self.assertIn('[node name="Main" type="MarginContainer" groups=["scene_flow"]]', main_scene_text)
            self.assertIn('[node name="Intro" type="MarginContainer"]', intro_scene_text)
            self.assertIn('[node name="Fader" type="MarginContainer"]', fader_scene_text)
            self.assertIn("SceneChanger.go_to_intro()", main_script_text)
            self.assertIn('AudioManager.play_cue("start")', main_script_text)
            self.assertIn("AudioManager.describe_state()", main_script_text)
            self.assertIn("Start pressed. %s", main_script_text)
            self.assertIn("func change_scene(path: String) -> void:", scene_changer_text)

            manifest = json.loads((build_dir / ".pygodot" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": True,
                        "id": "Script_scripts_audio_manager_gd",
                        "ownership": "copied",
                        "path": "res://scripts/audio_manager.gd",
                        "type": "Script",
                    },
                    {
                        "copied": False,
                        "id": "Script_scripts_fader_gd",
                        "ownership": "generated",
                        "path": "res://scripts/fader.gd",
                        "type": "Script",
                    },
                    {
                        "copied": False,
                        "id": "Script_scripts_intro_gd",
                        "ownership": "generated",
                        "path": "res://scripts/intro.gd",
                        "type": "Script",
                    },
                    {
                        "copied": False,
                        "id": "Script_scripts_main_gd",
                        "ownership": "generated",
                        "path": "res://scripts/main.gd",
                        "type": "Script",
                    },
                    {
                        "copied": True,
                        "id": "Script_scripts_scene_changer_gd",
                        "ownership": "copied",
                        "path": "res://scripts/scene_changer.gd",
                        "type": "Script",
                    },
                ],
            )

    def test_ld49_unit_card_example_builds_animated_sprite_resources(self) -> None:
        unit_card = _load_example_game("ld49_unit_card")

        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            unit_card.game.build_dir = build_dir

            result = unit_card.game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/main.tscn",
                    "scenes/unit.tscn",
                    "scripts/unit.gd",
                ],
            )
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.copied_resources),
                ["assets/tone.wav", "assets/unit_atlas.svg"],
            )

            main_scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            scene_text = (build_dir / "scenes" / "unit.tscn").read_text(encoding="utf-8")
            script_text = (build_dir / "scripts" / "unit.gd").read_text(encoding="utf-8")
            self.assertIn(
                '[ext_resource type="PackedScene" path="res://scenes/unit.tscn" '
                'id="PackedScene_scenes_unit_tscn"]',
                main_scene_text,
            )
            self.assertIn('[node name="UnitField" type="Node2D"]', main_scene_text)
            self.assertIn(
                '[node name="UnitA" parent="." instance=ExtResource("PackedScene_scenes_unit_tscn")]',
                main_scene_text,
            )
            self.assertIn(
                '[node name="UnitB" parent="." instance=ExtResource("PackedScene_scenes_unit_tscn")]',
                main_scene_text,
            )
            self.assertIn(
                '[node name="UnitC" parent="." instance=ExtResource("PackedScene_scenes_unit_tscn")]',
                main_scene_text,
            )
            self.assertIn('[sub_resource type="AtlasTexture" id="AtlasTexture_unit_idle_0"]', scene_text)
            self.assertIn('[sub_resource type="SpriteFrames" id="SpriteFrames_unit_frames"]', scene_text)
            self.assertIn('[sub_resource type="RectangleShape2D" id="RectangleShape2D_rectangle_96_96"]', scene_text)
            self.assertIn('"name": &"idle"', scene_text)
            self.assertIn('"texture": SubResource("AtlasTexture_unit_idle_0")', scene_text)
            self.assertIn('[node name="Unit" type="Area2D"]', scene_text)
            self.assertIn('[node name="AnimatedUnit" type="AnimatedSprite2D" parent="."]', scene_text)
            self.assertIn('[node name="ClickShape" type="CollisionShape2D" parent="."]', scene_text)
            self.assertIn('sprite_frames = SubResource("SpriteFrames_unit_frames")', scene_text)
            self.assertIn('[node name="SpawnAudio" type="AudioStreamPlayer" parent="."]', scene_text)
            self.assertIn('[node name="DeathAudio" type="AudioStreamPlayer" parent="."]', scene_text)
            self.assertIn(
                '[connection signal="input_event" from="." to="." method="_on_unit_input_event"]',
                scene_text,
            )
            self.assertIn('sprite.play("idle")', script_text)
            self.assertIn("func play_spawn() -> void:", script_text)
            self.assertIn("spawn_audio.play()", script_text)
            self.assertIn("func play_death() -> void:", script_text)
            self.assertIn("func _on_unit_input_event(", script_text)
            self.assertIn("play_death()", script_text)

            manifest = json.loads((build_dir / ".pygodot" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": True,
                        "id": "AudioStream_assets_tone_wav",
                        "ownership": "copied",
                        "path": "res://assets/tone.wav",
                        "type": "AudioStream",
                    },
                    {
                        "copied": False,
                        "id": "PackedScene_scenes_unit_tscn",
                        "ownership": "generated",
                        "path": "res://scenes/unit.tscn",
                        "type": "PackedScene",
                    },
                    {
                        "copied": False,
                        "id": "Script_scripts_unit_gd",
                        "ownership": "generated",
                        "path": "res://scripts/unit.gd",
                        "type": "Script",
                    },
                    {
                        "copied": True,
                        "id": "Texture2D_assets_unit_atlas_svg",
                        "ownership": "copied",
                        "path": "res://assets/unit_atlas.svg",
                        "type": "Texture2D",
                    },
                ],
            )
