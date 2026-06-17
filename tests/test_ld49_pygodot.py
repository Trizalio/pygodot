from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ld49_pygodot.game import game


class LD49PygodotSkeletonTests(unittest.TestCase):
    def test_stage_b_skeleton_builds_game_scene_shell(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game.build_dir = build_dir

            result = game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/fader.tscn",
                    "scenes/hint.tscn",
                    "scenes/intro.tscn",
                    "scenes/main.tscn",
                    "scripts/fader.gd",
                    "scripts/intro.gd",
                    "scripts/main.gd",
                ],
            )
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.copied_resources),
                [
                    "resources/icon.svg",
                    "scripts/audio_manager.gd",
                    "scripts/game_state.gd",
                    "scripts/scene_changer.gd",
                ],
            )
            self.assertEqual(result.generated_resources, [])
            self.assertEqual(result.referenced_resources, [])

            project_text = (build_dir / "project.godot").read_text(encoding="utf-8")
            main_scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            hint_scene_text = (build_dir / "scenes" / "hint.tscn").read_text(encoding="utf-8")
            intro_scene_text = (build_dir / "scenes" / "intro.tscn").read_text(encoding="utf-8")
            fader_scene_text = (build_dir / "scenes" / "fader.tscn").read_text(encoding="utf-8")
            main_script_text = (build_dir / "scripts" / "main.gd").read_text(encoding="utf-8")
            scene_changer_text = (build_dir / "scripts" / "scene_changer.gd").read_text(encoding="utf-8")
            audio_manager_text = (build_dir / "scripts" / "audio_manager.gd").read_text(encoding="utf-8")

            self.assertIn('config/name="LD49Pygodot"', project_text)
            self.assertIn('run/main_scene="res://scenes/main.tscn"', project_text)
            self.assertIn('config/icon="res://resources/icon.svg"', project_text)
            self.assertIn("[autoload]", project_text)
            self.assertIn('GameState="*res://scripts/game_state.gd"', project_text)
            self.assertIn('SceneChanger="*res://scripts/scene_changer.gd"', project_text)
            self.assertIn('AudioManager="*res://scripts/audio_manager.gd"', project_text)
            self.assertIn("window/size/viewport_width=540", project_text)
            self.assertIn("window/stretch/mode=\"canvas_items\"", project_text)
            self.assertIn("[audio]", project_text)
            self.assertIn("output_latency/web=200", project_text)
            self.assertIn("[physics]", project_text)
            self.assertIn("common/enable_pause_aware_picking=true", project_text)

            self.assertIn('[node name="Main" type="MarginContainer" groups=["ld49_port", "stage_b"]]', main_scene_text)
            self.assertIn('[node name="Background" type="TextureRect" parent="."]', main_scene_text)
            self.assertIn('texture = ExtResource("Texture2D_resources_icon_svg")', main_scene_text)
            self.assertIn('[node name="ScorePanel" type="HBoxContainer" parent="Shell/VBox"]', main_scene_text)
            self.assertIn('[node name="ScoreLabel" type="Label" parent="Shell/VBox/ScorePanel"]', main_scene_text)
            self.assertIn('[node name="TurnLabel" type="Label" parent="Shell/VBox/ScorePanel"]', main_scene_text)
            self.assertIn('[node name="MapGrid" type="GridContainer" parent="Shell/VBox/GameBody"]', main_scene_text)
            self.assertIn("columns = 5", main_scene_text)
            self.assertEqual(main_scene_text.count('type="Panel" parent="Shell/VBox/GameBody/MapGrid"'), 25)
            self.assertIn('[node name="TileA1" type="Panel" parent="Shell/VBox/GameBody/MapGrid"]', main_scene_text)
            self.assertIn('[node name="TileE5" type="Panel" parent="Shell/VBox/GameBody/MapGrid"]', main_scene_text)
            self.assertIn('[node name="SpellsPanel" type="VBoxContainer" parent="Shell/VBox/GameBody/SidePanel"]', main_scene_text)
            self.assertIn('[node name="FireballButton" type="Button" parent="Shell/VBox/GameBody/SidePanel/SpellsPanel"]', main_scene_text)
            self.assertIn('[node name="HintPanel" parent="Shell/VBox/GameBody/SidePanel" instance=ExtResource("PackedScene_scenes_hint_tscn")]', main_scene_text)
            self.assertIn('[node name="Hint" type="Panel"]', hint_scene_text)
            self.assertIn('[node name="Intro" type="MarginContainer" groups=["ld49_port", "stage_a"]]', intro_scene_text)
            self.assertIn('[node name="Fader" type="MarginContainer" groups=["ld49_port", "stage_a"]]', fader_scene_text)
            self.assertIn(
                '[connection signal="pressed" from="Shell/VBox/DebugBar/IntroButton" to="." method="_on_intro_pressed"]',
                main_scene_text,
            )
            self.assertIn(
                '[connection signal="pressed" from="Shell/VBox/DebugBar/FaderButton" to="." method="_on_fader_pressed"]',
                main_scene_text,
            )
            self.assertIn(
                '[connection signal="pressed" from="Shell/VBox/DebugBar/ResetButton" to="." method="_on_reset_pressed"]',
                main_scene_text,
            )
            self.assertIn("SceneChanger.go_to_intro()", main_script_text)
            self.assertIn("SceneChanger.show_fader()", main_script_text)
            self.assertIn("func _on_reset_pressed() -> void:", main_script_text)
            self.assertIn("const INTRO_SCENE := \"res://scenes/intro.tscn\"", scene_changer_text)
            self.assertIn("func play_cue(name: String) -> void:", audio_manager_text)

            manifest = json.loads((build_dir / ".pygodot" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["external_resources"],
                [
                    {
                        "copied": False,
                        "id": "PackedScene_scenes_hint_tscn",
                        "ownership": "generated",
                        "path": "res://scenes/hint.tscn",
                        "type": "PackedScene",
                    },
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
                        "copied": True,
                        "id": "Script_scripts_game_state_gd",
                        "ownership": "copied",
                        "path": "res://scripts/game_state.gd",
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
                    {
                        "copied": True,
                        "id": "Texture2D_resources_icon_svg",
                        "ownership": "copied",
                        "path": "res://resources/icon.svg",
                        "type": "Texture2D",
                    },
                ],
            )


if __name__ == "__main__":
    unittest.main()
