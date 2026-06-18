@onready var status_label := $Shell/VBox/ScorePanel/StatusLabel
@onready var score_label := $Shell/VBox/ScorePanel/ScoreLabel
@onready var turn_label := $Shell/VBox/ScorePanel/TurnLabel
@onready var castle_label := $Shell/VBox/GameBody/BoardPanel/CastlePanel/CastleLabel
@onready var map_grid := $Shell/VBox/GameBody/BoardPanel/MapGrid
var turn_playback_active := false

func _ready() -> void:
    GameState.reset()
    AudioManager.play_cue("main_ready")
    _connect_tiles()
    _refresh_tiles()
    _refresh_runtime_labels()

func _on_intro_pressed() -> void:
    AudioManager.play_cue("open_intro")
    SceneChanger.go_to_intro()

func _on_fader_pressed() -> void:
    AudioManager.play_cue("open_fader")
    SceneChanger.show_fader()

func _on_reset_pressed() -> void:
    if turn_playback_active:
        return
    GameState.reset()
    _reset_tiles()
    _refresh_tiles()
    AudioManager.stop_music()
    _refresh_runtime_labels()

func _on_advance_units_pressed() -> void:
    if turn_playback_active:
        return
    await _play_turn_phases("Pass")

func _on_tile_spell_dropped(tile_id: String, spell_id: String, display_name: String) -> void:
    if turn_playback_active:
        return
    turn_playback_active = true
    _clear_spell_preview()
    var summary := GameState.apply_spell(tile_id, spell_id)
    AudioManager.play_cue("cast_%s" % spell_id)
    status_label.text = "%s cast on %s. %s" % [display_name, tile_id, summary]
    _refresh_tiles()
    _refresh_counters()
    await _pause_turn_phase()
    await _play_turn_phases(display_name)

func _play_turn_phases(action_name: String) -> void:
    turn_playback_active = true
    GameState.begin_neighbor_phase()
    if not GameState.has_queued_neighbor_event():
        status_label.text = "%s: no neighbor effects" % action_name
        _refresh_tiles()
        _refresh_counters()
        await _pause_turn_phase()
    while GameState.has_queued_neighbor_event():
        var event := GameState.peek_neighbor_event()
        _show_neighbor_event(event)
        status_label.text = "%s: %s -> %s (%s)" % [
            action_name,
            event.get("actor_name", ""),
            event.get("target_name", ""),
            event.get("effect", ""),
        ]
        _refresh_counters()
        await _pause_unit_step()
        var trait_result := GameState.resolve_next_neighbor_event()
        status_label.text = "%s: %s" % [action_name, trait_result]
        _refresh_tiles()
        _refresh_counters()
        await _pause_unit_step()
    _clear_focus_preview()
    GameState.begin_movement_phase()
    AudioManager.play_cue("units_move")
    while GameState.has_queued_movement():
        var preview := GameState.peek_next_unit_move()
        _show_next_movement_preview(preview)
        if not preview.is_empty():
            status_label.text = "%s: next %s %s -> %s" % [
                action_name,
                preview.get("display_name", ""),
                preview.get("from", ""),
                preview.get("to", ""),
            ]
            _refresh_counters()
            await _pause_unit_step()
        var moved := GameState.move_next_unit()
        if moved.is_empty():
            continue
        status_label.text = "%s: %s" % [action_name, moved]
        _refresh_tiles()
        _refresh_counters()
        await _pause_unit_step()
    _clear_focus_preview()
    var spawned := GameState.spawn_wave()
    status_label.text = "%s: %s" % [action_name, spawned]
    _refresh_tiles()
    _refresh_counters()
    _finish_if_complete()
    turn_playback_active = false

func _pause_turn_phase() -> void:
    await get_tree().create_timer(0.45).timeout

func _pause_unit_step() -> void:
    await get_tree().create_timer(0.24).timeout

func _connect_tiles() -> void:
    for tile in map_grid.get_children():
        if tile.has_signal("spell_dropped") and not tile.spell_dropped.is_connected(_on_tile_spell_dropped):
            tile.spell_dropped.connect(_on_tile_spell_dropped)
        if tile.has_signal("spell_hovered") and not tile.spell_hovered.is_connected(_on_tile_spell_hovered):
            tile.spell_hovered.connect(_on_tile_spell_hovered)
        if tile.has_signal("spell_hover_ended") and not tile.spell_hover_ended.is_connected(_clear_spell_preview):
            tile.spell_hover_ended.connect(_clear_spell_preview)

func _reset_tiles() -> void:
    for tile in map_grid.get_children():
        if tile.has_method("reset_state"):
            tile.reset_state()

func _refresh_tiles() -> void:
    for tile in map_grid.get_children():
        if tile.has_method("clear_unit"):
            tile.clear_unit()
        var unit := GameState.unit_at(tile.tile_id)
        if not unit.is_empty() and tile.has_method("set_unit"):
            tile.set_unit(unit["display_name"], unit["hp"], unit["status"])

func _on_tile_spell_hovered(tile_id: String, spell_id: String) -> void:
    if turn_playback_active:
        return
    _clear_spell_preview()
    var targets := GameState.preview_spell_targets(tile_id, spell_id)
    for target_id in targets:
        var tile := _tile_by_id(target_id)
        if tile == null or not tile.has_method("set_preview"):
            continue
        var role := "area"
        if target_id == tile_id:
            role = "primary"
        tile.set_preview(role, spell_id)
    if targets.size() > 1:
        status_label.text = "%s will affect %d cells" % [spell_id.capitalize(), targets.size()]
    else:
        status_label.text = "%s targets %s" % [spell_id.capitalize(), tile_id]

func _clear_spell_preview() -> void:
    for tile in map_grid.get_children():
        if tile.has_method("clear_preview"):
            tile.clear_preview()

func _show_neighbor_event(event: Dictionary) -> void:
    _clear_focus_preview()
    var actor_tile := _tile_by_id(str(event.get("actor_cell", "")))
    if actor_tile != null and actor_tile.has_method("set_focus_preview"):
        actor_tile.set_focus_preview("actor", str(event.get("actor_name", "")), str(event.get("effect", "")))
    var target_tile := _tile_by_id(str(event.get("target_cell", "")))
    if target_tile != null and target_tile.has_method("set_focus_preview"):
        target_tile.set_focus_preview("target", str(event.get("target_name", "")), str(event.get("effect", "")))

func _show_next_movement_preview(preview: Dictionary) -> void:
    _clear_focus_preview()
    if preview.is_empty():
        return
    var from_tile := _tile_by_id(str(preview.get("from", "")))
    if from_tile != null and from_tile.has_method("set_movement_preview"):
        from_tile.set_movement_preview("from", str(preview.get("outcome", "")), str(preview.get("display_name", "")))
    var from_cell := str(preview.get("from", ""))
    var to_cell := str(preview.get("to", ""))
    if to_cell == "CASTLE" or to_cell.is_empty() or to_cell == from_cell:
        return
    var to_tile := _tile_by_id(to_cell)
    if to_tile != null and to_tile.has_method("set_movement_preview"):
        to_tile.set_movement_preview("to", str(preview.get("outcome", "")), str(preview.get("display_name", "")))

func _clear_focus_preview() -> void:
    for tile in map_grid.get_children():
        if tile.has_method("clear_preview"):
            tile.clear_preview()

func _tile_by_id(tile_id: String) -> Node:
    for tile in map_grid.get_children():
        if str(tile.tile_id) == tile_id:
            return tile
    return null

func _finish_if_complete() -> void:
    if GameState.is_complete():
        AudioManager.play_cue("battle_complete")
        SceneChanger.go_to_end()

func _refresh_runtime_labels() -> void:
    status_label.text = "%s. %s. %s" % [
        GameState.describe_state(),
        GameState.describe_matrix(),
        AudioManager.describe_state(),
    ]
    _refresh_counters()

func _refresh_counters() -> void:
    score_label.text = GameState.describe_score()
    turn_label.text = GameState.describe_turn()
    castle_label.text = GameState.describe_castle()
