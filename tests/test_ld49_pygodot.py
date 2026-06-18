from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ld49_pygodot.game import game
from ld49_pygodot.validation import validate_build


class LD49PygodotPortTests(unittest.TestCase):
    def test_ld49_port_builds_stage_a_to_g_vertical_slice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game.build_dir = build_dir

            result = game.build()

            self.assertEqual(
                sorted(path.relative_to(build_dir).as_posix() for path in result.written_files),
                [
                    ".pygodot/manifest.json",
                    "project.godot",
                    "scenes/end.tscn",
                    "scenes/fader.tscn",
                    "scenes/hint.tscn",
                    "scenes/intro.tscn",
                    "scenes/main.tscn",
                    "scenes/spell.tscn",
                    "scenes/tile.tscn",
                    "scenes/unit.tscn",
                    "scripts/end.gd",
                    "scripts/fader.gd",
                    "scripts/intro.gd",
                    "scripts/main.gd",
                    "scripts/spell.gd",
                    "scripts/tile.gd",
                    "scripts/unit.gd",
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
            end_scene_text = (build_dir / "scenes" / "end.tscn").read_text(encoding="utf-8")
            hint_scene_text = (build_dir / "scenes" / "hint.tscn").read_text(encoding="utf-8")
            spell_scene_text = (build_dir / "scenes" / "spell.tscn").read_text(encoding="utf-8")
            tile_scene_text = (build_dir / "scenes" / "tile.tscn").read_text(encoding="utf-8")
            unit_scene_text = (build_dir / "scenes" / "unit.tscn").read_text(encoding="utf-8")
            intro_scene_text = (build_dir / "scenes" / "intro.tscn").read_text(encoding="utf-8")
            fader_scene_text = (build_dir / "scenes" / "fader.tscn").read_text(encoding="utf-8")
            end_script_text = (build_dir / "scripts" / "end.gd").read_text(encoding="utf-8")
            main_script_text = (build_dir / "scripts" / "main.gd").read_text(encoding="utf-8")
            spell_script_text = (build_dir / "scripts" / "spell.gd").read_text(encoding="utf-8")
            tile_script_text = (build_dir / "scripts" / "tile.gd").read_text(encoding="utf-8")
            unit_script_text = (build_dir / "scripts" / "unit.gd").read_text(encoding="utf-8")
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
            self.assertIn("window/size/viewport_width=820", project_text)
            self.assertIn("window/size/viewport_height=760", project_text)
            self.assertIn("window/stretch/mode=\"canvas_items\"", project_text)
            self.assertIn("[audio]", project_text)
            self.assertIn("output_latency/web=200", project_text)
            self.assertIn("[physics]", project_text)
            self.assertIn("common/enable_pause_aware_picking=true", project_text)

            self.assertIn('[node name="Main" type="MarginContainer" groups=["ld49_port", "stage_a_g"]]', main_scene_text)
            self.assertIn('[node name="Background" type="TextureRect" parent="."]', main_scene_text)
            self.assertIn('texture = ExtResource("Texture2D_resources_icon_svg")', main_scene_text)
            self.assertIn('[node name="ScorePanel" type="HBoxContainer" parent="Shell/VBox"]', main_scene_text)
            self.assertIn('[node name="ScoreLabel" type="Label" parent="Shell/VBox/ScorePanel"]', main_scene_text)
            self.assertIn('[node name="TurnLabel" type="Label" parent="Shell/VBox/ScorePanel"]', main_scene_text)
            self.assertIn('[node name="CastlePanel" type="Panel" parent="Shell/VBox/GameBody/BoardPanel"]', main_scene_text)
            self.assertIn('text = "Castle 0/6 D:0 U:0 G:0"', main_scene_text)
            self.assertIn('[node name="MapGrid" type="GridContainer" parent="Shell/VBox/GameBody/BoardPanel"]', main_scene_text)
            self.assertIn("columns = 5", main_scene_text)
            self.assertIn("custom_minimum_size = Vector2(520, 430)", main_scene_text)
            self.assertEqual(main_scene_text.count('instance=ExtResource("PackedScene_scenes_tile_tscn")'), 25)
            self.assertIn('[node name="TileA1" parent="Shell/VBox/GameBody/BoardPanel/MapGrid" instance=ExtResource("PackedScene_scenes_tile_tscn")]', main_scene_text)
            self.assertIn('[node name="TileE5" parent="Shell/VBox/GameBody/BoardPanel/MapGrid" instance=ExtResource("PackedScene_scenes_tile_tscn")]', main_scene_text)
            self.assertIn('[node name="SidePanel" type="VBoxContainer" parent="Shell/VBox/GameBody"]', main_scene_text)
            self.assertIn("custom_minimum_size = Vector2(220, 360)", main_scene_text)
            self.assertIn('[node name="SpellsPanel" type="VBoxContainer" parent="Shell/VBox/GameBody/SidePanel"]', main_scene_text)
            self.assertIn('[node name="FireballSpell" parent="Shell/VBox/GameBody/SidePanel/SpellsPanel" instance=ExtResource("PackedScene_scenes_spell_tscn")]', main_scene_text)
            self.assertIn('spell_id = "fireball"', main_scene_text)
            self.assertIn('[node name="FrostSpell" parent="Shell/VBox/GameBody/SidePanel/SpellsPanel" instance=ExtResource("PackedScene_scenes_spell_tscn")]', main_scene_text)
            self.assertIn('spell_id = "frost"', main_scene_text)
            self.assertIn('[node name="ShieldSpell" parent="Shell/VBox/GameBody/SidePanel/SpellsPanel" instance=ExtResource("PackedScene_scenes_spell_tscn")]', main_scene_text)
            self.assertIn('spell_id = "shield"', main_scene_text)
            self.assertIn('[node name="HealSpell" parent="Shell/VBox/GameBody/SidePanel/SpellsPanel" instance=ExtResource("PackedScene_scenes_spell_tscn")]', main_scene_text)
            self.assertIn('spell_id = "heal"', main_scene_text)
            self.assertIn('hint_text = "restore hp"', main_scene_text)
            self.assertNotIn("UnitsPanel", main_scene_text)
            self.assertNotIn("PackedScene_scenes_unit_tscn", main_scene_text)
            self.assertIn('[node name="AdvanceUnitsButton" type="Button" parent="Shell/VBox/DebugBar"]', main_scene_text)
            self.assertIn('text = "Pass Turn"', main_scene_text)
            self.assertIn("custom_minimum_size = Vector2(170, 42)", main_scene_text)
            self.assertIn('[node name="HintPanel" parent="Shell/VBox/GameBody/SidePanel" instance=ExtResource("PackedScene_scenes_hint_tscn")]', main_scene_text)
            self.assertIn('[node name="Hint" type="Panel"]', hint_scene_text)
            self.assertIn("custom_minimum_size = Vector2(200, 72)", hint_scene_text)
            self.assertIn("clip_text = true", hint_scene_text)
            self.assertIn('[node name="End" type="MarginContainer" groups=["ld49_port", "stage_f"]]', end_scene_text)
            self.assertIn('[connection signal="pressed" from="Panel/VBox/BackButton" to="." method="_on_back_pressed"]', end_scene_text)
            self.assertIn('[node name="Spell" type="Panel"]', spell_scene_text)
            self.assertIn('[node name="Tile" type="Panel"]', tile_scene_text)
            self.assertIn('[node name="Unit" type="Label" parent="VBox"]', tile_scene_text)
            self.assertIn("custom_minimum_size = Vector2(88, 24)", tile_scene_text)
            self.assertIn("clip_text = true", tile_scene_text)
            self.assertIn('[node name="Unit" type="Panel"]', unit_scene_text)
            self.assertIn('[node name="Intro" type="MarginContainer" groups=["ld49_port", "stage_a_g"]]', intro_scene_text)
            self.assertIn('[node name="Fader" type="MarginContainer" groups=["ld49_port", "stage_a_g"]]', fader_scene_text)
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
            self.assertIn(
                '[connection signal="pressed" from="Shell/VBox/DebugBar/AdvanceUnitsButton" to="." method="_on_advance_units_pressed"]',
                main_scene_text,
            )
            self.assertIn("SceneChanger.go_to_intro()", main_script_text)
            self.assertIn("SceneChanger.show_fader()", main_script_text)
            self.assertIn("SceneChanger.go_to_end()", main_script_text)
            self.assertIn("GameState.describe_castle()", main_script_text)
            self.assertIn("func _finish_if_complete() -> void:", main_script_text)
            self.assertIn("func _on_reset_pressed() -> void:", main_script_text)
            self.assertIn("var turn_playback_active := false", main_script_text)
            self.assertIn("func _play_turn_phases(action_name: String) -> void:", main_script_text)
            self.assertIn("func _pause_turn_phase() -> void:", main_script_text)
            self.assertIn("await get_tree().create_timer(0.45).timeout", main_script_text)
            self.assertIn("func _pause_unit_step() -> void:", main_script_text)
            self.assertIn("await get_tree().create_timer(0.24).timeout", main_script_text)
            self.assertIn("GameState.begin_neighbor_phase()", main_script_text)
            self.assertIn("GameState.has_queued_neighbor_event()", main_script_text)
            self.assertIn("GameState.peek_neighbor_event()", main_script_text)
            self.assertIn("GameState.resolve_next_neighbor_event()", main_script_text)
            self.assertIn("GameState.begin_movement_phase()", main_script_text)
            self.assertIn("GameState.has_queued_movement()", main_script_text)
            self.assertIn("GameState.peek_next_unit_move()", main_script_text)
            self.assertIn("GameState.move_next_unit()", main_script_text)
            self.assertIn("GameState.spawn_wave()", main_script_text)
            self.assertIn("func _refresh_counters() -> void:", main_script_text)
            self.assertIn("func _show_neighbor_event(event: Dictionary) -> void:", main_script_text)
            self.assertIn("func _show_next_movement_preview(preview: Dictionary) -> void:", main_script_text)
            self.assertIn("func _clear_focus_preview() -> void:", main_script_text)
            self.assertIn("func _on_tile_spell_hovered(tile_id: String, spell_id: String) -> void:", main_script_text)
            self.assertIn("func _clear_spell_preview() -> void:", main_script_text)
            self.assertIn("func _tile_by_id(tile_id: String) -> Node:", main_script_text)
            self.assertIn("GameState.preview_spell_targets(tile_id, spell_id)", main_script_text)
            self.assertIn("tile.spell_hovered.connect(_on_tile_spell_hovered)", main_script_text)
            self.assertIn("tile.spell_hover_ended.connect(_clear_spell_preview)", main_script_text)
            self.assertIn("func _connect_tiles() -> void:", main_script_text)
            self.assertIn("func _reset_tiles() -> void:", main_script_text)
            self.assertIn("tile.reset_state()", main_script_text)
            self.assertIn("func _on_advance_units_pressed() -> void:", main_script_text)
            self.assertNotIn("func _refresh_units() -> void:", main_script_text)
            self.assertIn("tile.spell_dropped.connect(_on_tile_spell_dropped)", main_script_text)
            self.assertIn("func _on_tile_spell_dropped(tile_id: String, spell_id: String, display_name: String) -> void:", main_script_text)
            self.assertIn("GameState.describe_matrix()", main_script_text)
            self.assertIn("func _get_drag_data(_at_position: Vector2) -> Variant:", spell_script_text)
            self.assertIn('"spell_id": spell_id', spell_script_text)
            self.assertIn('hint.text = hint_text', spell_script_text)
            self.assertIn("func _on_back_pressed() -> void:", end_script_text)
            self.assertIn("GameState.describe_score()", end_script_text)
            self.assertIn("func reset_state() -> void:", tile_script_text)
            self.assertIn("func _process(_delta: float) -> void:", tile_script_text)
            self.assertIn("get_global_rect().has_point(get_global_mouse_position())", tile_script_text)
            self.assertIn("signal spell_dropped(tile_id: String, spell_id: String, display_name: String)", tile_script_text)
            self.assertIn("signal spell_hovered(tile_id: String, spell_id: String)", tile_script_text)
            self.assertIn("signal spell_hover_ended()", tile_script_text)
            self.assertIn("func _can_drop_data(_at_position: Vector2, data: Variant) -> bool:", tile_script_text)
            self.assertIn("func _drop_data(_at_position: Vector2, data: Variant) -> void:", tile_script_text)
            self.assertIn("spell_hovered.emit(tile_id, spell_id)", tile_script_text)
            self.assertIn("spell_hover_ended.emit()", tile_script_text)
            self.assertIn("spell_dropped.emit(tile_id, spell_id, display_name)", tile_script_text)
            self.assertIn("func set_unit(display_name: String, hp: int, status: String) -> void:", tile_script_text)
            self.assertIn("func set_preview(role: String, spell_id: String) -> void:", tile_script_text)
            self.assertIn("func set_movement_preview(role: String, outcome: String, display_name: String) -> void:", tile_script_text)
            self.assertIn("func set_focus_preview(role: String, display_name: String, effect: String) -> void:", tile_script_text)
            self.assertIn("func clear_preview() -> void:", tile_script_text)
            self.assertIn("func _preview_color(spell_id: String) -> Color:", tile_script_text)
            self.assertIn("func _movement_preview_label(role: String, outcome: String, display_name: String) -> String:", tile_script_text)
            self.assertIn("func _movement_preview_color(role: String, outcome: String) -> Color:", tile_script_text)
            self.assertIn("func _focus_preview_label(role: String, display_name: String, effect: String) -> String:", tile_script_text)
            self.assertIn("func _focus_preview_color(role: String, effect: String) -> Color:", tile_script_text)
            self.assertIn("func _short_name(display_name: String) -> String:", tile_script_text)
            self.assertIn("func _status_color(status: String) -> Color:", tile_script_text)
            self.assertIn("_flash(_status_color(status))", tile_script_text)
            self.assertIn('unit_summary = "%s HP %d" % [display_name, hp]', tile_script_text)
            self.assertIn("func _status_label(status: String) -> String:", tile_script_text)
            self.assertIn("func apply_state(data: Dictionary) -> void:", unit_script_text)
            self.assertIn("shield = int(data.get(\"shield\", shield))", unit_script_text)
            self.assertIn("HP %d SH %d @ %s", unit_script_text)
            self.assertIn("func apply_spell(cell_id: String, spell_id: String) -> String:", game_state_text)
            self.assertIn("var castle_capacity := 6", game_state_text)
            self.assertIn("func resolve_turn() -> String:", game_state_text)
            self.assertIn("func resolve_neighbor_traits() -> String:", game_state_text)
            self.assertIn("func begin_neighbor_phase() -> void:", game_state_text)
            self.assertIn("func has_queued_neighbor_event() -> bool:", game_state_text)
            self.assertIn("func peek_neighbor_event() -> Dictionary:", game_state_text)
            self.assertIn("func resolve_next_neighbor_event() -> String:", game_state_text)
            self.assertIn("func move_units() -> String:", game_state_text)
            self.assertIn("func begin_movement_phase() -> Array:", game_state_text)
            self.assertIn("func has_queued_movement() -> bool:", game_state_text)
            self.assertIn("func peek_next_unit_move() -> Dictionary:", game_state_text)
            self.assertIn("func move_next_unit() -> String:", game_state_text)
            self.assertIn("func spawn_wave() -> String:", game_state_text)
            self.assertIn("func preview_spell_targets(cell_id: String, spell_id: String) -> Array[String]:", game_state_text)
            self.assertIn("func preview_unit_moves() -> Array:", game_state_text)
            self.assertIn("func describe_castle() -> String:", game_state_text)
            self.assertIn("func _spawn_wave() -> String:", game_state_text)
            self.assertIn("func _target_cells_for_spell(cell_id: String, spell_id: String) -> Array[String]:", game_state_text)
            self.assertIn("func _clash_units(attacker_id: String, blocker_id: String, cell_id: String) -> String:", game_state_text)
            self.assertIn("func _neighbor_events() -> Array:", game_state_text)
            self.assertIn("func _make_neighbor_event(actor_id: String, target_id: String, effect: String) -> Dictionary:", game_state_text)
            self.assertIn("func _apply_neighbor_event(event: Dictionary) -> String:", game_state_text)
            self.assertIn("func _neighbor_unit_ids(cell_id: String) -> Array[String]:", game_state_text)
            self.assertIn("func _has_neighbor_faction(unit_ids: Array[String], faction: String) -> bool:", game_state_text)
            self.assertIn("func _has_enemy_neighbor(unit_ids: Array[String], faction: String) -> bool:", game_state_text)
            self.assertIn("func _defeat_unit(unit_id: String, unit: Dictionary) -> void:", game_state_text)
            self.assertIn("var unit_order := 0", game_state_text)
            self.assertIn("var neighbor_queue: Array = []", game_state_text)
            self.assertIn("var movement_queue: Array = []", game_state_text)
            self.assertIn('"spawn_order": order', game_state_text)
            self.assertIn("movement_queue = _movement_order()", game_state_text)
            self.assertIn("func _move_unit(unit_id: String) -> String:", game_state_text)
            self.assertIn("func _movement_preview_for(unit_id: String) -> Dictionary:", game_state_text)
            self.assertIn("func _movement_order() -> Array:", game_state_text)
            self.assertIn("ordered.sort_custom(_younger_unit_first)", game_state_text)
            self.assertIn("func _younger_unit_first(left_id: String, right_id: String) -> bool:", game_state_text)
            self.assertIn("return left_order > right_order", game_state_text)
            self.assertIn('"scorched"', game_state_text)
            self.assertIn('"horde"', game_state_text)
            self.assertIn('"braced"', game_state_text)
            self.assertIn('"stacked"', game_state_text)
            self.assertIn('"raging"', game_state_text)
            self.assertIn("for unit_id in units.keys():", game_state_text)
            self.assertIn("units.erase(unit_id)", game_state_text)
            self.assertNotIn('unit["status"] = "escaped"', game_state_text)
            self.assertIn('"imp": _make_unit("imp", "Imp", "demon", "B1", 4)', game_state_text)
            self.assertIn('"bones": _make_unit("bones", "Bones", "undead", "C3", 5)', game_state_text)
            self.assertIn('"gob": _make_unit("gob", "Gob", "greenskin", "E1", 3)', game_state_text)
            self.assertIn("func advance_units() -> String:", game_state_text)
            self.assertIn("func is_complete() -> bool:", game_state_text)
            self.assertIn("func _apply_spell_to_unit(unit_id: String, spell_id: String, cell_id: String) -> String:", game_state_text)
            self.assertIn('"frost":', game_state_text)
            self.assertIn('"shield":', game_state_text)
            self.assertIn('"heal":', game_state_text)
            self.assertIn("func _tick_status(unit_id: String) -> String:", game_state_text)
            self.assertIn("func _damage_unit(unit: Dictionary, amount: int) -> void:", game_state_text)
            self.assertIn("func unit_at(cell_id: String) -> Dictionary:", game_state_text)
            self.assertIn("func _enter_matrix(unit_id: String) -> void:", game_state_text)
            self.assertIn("func _exit_matrix(unit_id: String) -> void:", game_state_text)
            self.assertIn('unit["status"] = "burning"', game_state_text)
            self.assertIn('return "Scorch"', tile_script_text)
            self.assertIn('return "Horde"', tile_script_text)
            self.assertIn('return "Braced"', tile_script_text)
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
                        "id": "Script_scripts_end_gd",
                        "ownership": "generated",
                        "path": "res://scripts/end.gd",
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
                        "copied": False,
                        "id": "Script_scripts_unit_gd",
                        "ownership": "generated",
                        "path": "res://scripts/unit.gd",
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

    def test_stage_g_validation_accepts_generated_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game.build_dir = build_dir

            game.build()

            self.assertEqual(validate_build(build_dir), [])

    def test_stage_g_validation_reports_missing_required_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            build_dir = Path(tmp) / "godot_project"
            game.build_dir = build_dir

            game.build()
            (build_dir / "scenes" / "unit.tscn").unlink()

            self.assertIn("missing required file: scenes/unit.tscn", validate_build(build_dir))


if __name__ == "__main__":
    unittest.main()
