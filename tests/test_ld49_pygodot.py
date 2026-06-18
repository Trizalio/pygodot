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
                    "scenes/spell.tscn",
                    "scenes/tile.tscn",
                    "scripts/fader.gd",
                    "scripts/intro.gd",
                    "scripts/main.gd",
                    "scripts/spell.gd",
                    "scripts/tile.gd",
                ],
            )
            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.copied_resources),
                [
                    "resources/icon.svg",
                    "scripts/audio_manager.gd",
                    "scripts/game_state.gd",
                    "scripts/matrix.gd",
                    "scripts/matrix_utils.gd",
                    "scripts/rand.gd",
                    "scripts/scene_changer.gd",
                    "scripts/utils.gd",
                ],
            )
            self.assertEqual(result.generated_resources, [])
            self.assertEqual(result.referenced_resources, [])

            project_text = (build_dir / "project.godot").read_text(encoding="utf-8")
            main_scene_text = (build_dir / "scenes" / "main.tscn").read_text(encoding="utf-8")
            hint_scene_text = (build_dir / "scenes" / "hint.tscn").read_text(encoding="utf-8")
            spell_scene_text = (build_dir / "scenes" / "spell.tscn").read_text(encoding="utf-8")
            tile_scene_text = (build_dir / "scenes" / "tile.tscn").read_text(encoding="utf-8")
            intro_scene_text = (build_dir / "scenes" / "intro.tscn").read_text(encoding="utf-8")
            fader_scene_text = (build_dir / "scenes" / "fader.tscn").read_text(encoding="utf-8")
            main_script_text = (build_dir / "scripts" / "main.gd").read_text(encoding="utf-8")
            spell_script_text = (build_dir / "scripts" / "spell.gd").read_text(encoding="utf-8")
            tile_script_text = (build_dir / "scripts" / "tile.gd").read_text(encoding="utf-8")
            game_state_text = (build_dir / "scripts" / "game_state.gd").read_text(encoding="utf-8")
            matrix_text = (build_dir / "scripts" / "matrix.gd").read_text(encoding="utf-8")
            matrix_utils_text = (build_dir / "scripts" / "matrix_utils.gd").read_text(encoding="utf-8")
            rand_text = (build_dir / "scripts" / "rand.gd").read_text(encoding="utf-8")
            utils_text = (build_dir / "scripts" / "utils.gd").read_text(encoding="utf-8")
            scene_changer_text = (build_dir / "scripts" / "scene_changer.gd").read_text(encoding="utf-8")
            audio_manager_text = (build_dir / "scripts" / "audio_manager.gd").read_text(encoding="utf-8")

            self.assertIn('config/name="LD49Pygodot"', project_text)
            self.assertIn('run/main_scene="res://scenes/main.tscn"', project_text)
            self.assertIn('config/icon="res://resources/icon.svg"', project_text)
            self.assertIn("[autoload]", project_text)
            self.assertIn('Matrix="*res://scripts/matrix.gd"', project_text)
            self.assertIn('MatrixUtils="*res://scripts/matrix_utils.gd"', project_text)
            self.assertIn('Rand="*res://scripts/rand.gd"', project_text)
            self.assertIn('Utils="*res://scripts/utils.gd"', project_text)
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
            self.assertEqual(main_scene_text.count('instance=ExtResource("PackedScene_scenes_tile_tscn")'), 25)
            self.assertIn('[node name="TileA1" parent="Shell/VBox/GameBody/MapGrid" instance=ExtResource("PackedScene_scenes_tile_tscn")]', main_scene_text)
            self.assertIn('[node name="TileE5" parent="Shell/VBox/GameBody/MapGrid" instance=ExtResource("PackedScene_scenes_tile_tscn")]', main_scene_text)
            self.assertIn('[node name="SpellsPanel" type="VBoxContainer" parent="Shell/VBox/GameBody/SidePanel"]', main_scene_text)
            self.assertIn('[node name="FireballSpell" parent="Shell/VBox/GameBody/SidePanel/SpellsPanel" instance=ExtResource("PackedScene_scenes_spell_tscn")]', main_scene_text)
            self.assertIn('spell_id = "fireball"', main_scene_text)
            self.assertIn('[node name="HintPanel" parent="Shell/VBox/GameBody/SidePanel" instance=ExtResource("PackedScene_scenes_hint_tscn")]', main_scene_text)
            self.assertIn('[node name="Hint" type="Panel"]', hint_scene_text)
            self.assertIn('[node name="Spell" type="Panel"]', spell_scene_text)
            self.assertIn('[node name="Tile" type="Panel"]', tile_scene_text)
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
            self.assertIn("func _connect_tiles() -> void:", main_script_text)
            self.assertIn("tile.spell_dropped.connect(_on_tile_spell_dropped)", main_script_text)
            self.assertIn("func _on_tile_spell_dropped(tile_id: String, spell_id: String, display_name: String) -> void:", main_script_text)
            self.assertIn("GameState.describe_matrix()", main_script_text)
            self.assertIn("func _get_drag_data(_at_position: Vector2) -> Variant:", spell_script_text)
            self.assertIn('"spell_id": spell_id', spell_script_text)
            self.assertIn("signal spell_dropped(tile_id: String, spell_id: String, display_name: String)", tile_script_text)
            self.assertIn("func _can_drop_data(_at_position: Vector2, data: Variant) -> bool:", tile_script_text)
            self.assertIn("func _drop_data(_at_position: Vector2, data: Variant) -> void:", tile_script_text)
            self.assertIn("spell_dropped.emit(tile_id, spell_id, display_name)", tile_script_text)
            self.assertIn("func apply_spell(cell_id: String, spell_id: String) -> String:", game_state_text)
            self.assertIn("Matrix.reset(5, 5)", game_state_text)
            self.assertIn("func set_cell(cell_id: String, value: Variant) -> void:", matrix_text)
            self.assertIn("func neighbors(cell: String, width: int, height: int) -> Array[String]:", matrix_utils_text)
            self.assertIn("func choose(items: Array) -> Variant:", rand_text)
            self.assertIn("func describe_spell_drop(spell_id: String, cell_id: String) -> String:", utils_text)
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
                        "copied": False,
                        "id": "PackedScene_scenes_spell_tscn",
                        "ownership": "generated",
                        "path": "res://scenes/spell.tscn",
                        "type": "PackedScene",
                    },
                    {
                        "copied": False,
                        "id": "PackedScene_scenes_tile_tscn",
                        "ownership": "generated",
                        "path": "res://scenes/tile.tscn",
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
                        "id": "Script_scripts_matrix_gd",
                        "ownership": "copied",
                        "path": "res://scripts/matrix.gd",
                        "type": "Script",
                    },
                    {
                        "copied": True,
                        "id": "Script_scripts_matrix_utils_gd",
                        "ownership": "copied",
                        "path": "res://scripts/matrix_utils.gd",
                        "type": "Script",
                    },
                    {
                        "copied": True,
                        "id": "Script_scripts_rand_gd",
                        "ownership": "copied",
                        "path": "res://scripts/rand.gd",
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
                        "copied": False,
                        "id": "Script_scripts_spell_gd",
                        "ownership": "generated",
                        "path": "res://scripts/spell.gd",
                        "type": "Script",
                    },
                    {
                        "copied": False,
                        "id": "Script_scripts_tile_gd",
                        "ownership": "generated",
                        "path": "res://scripts/tile.gd",
                        "type": "Script",
                    },
                    {
                        "copied": True,
                        "id": "Script_scripts_utils_gd",
                        "ownership": "copied",
                        "path": "res://scripts/utils.gd",
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
