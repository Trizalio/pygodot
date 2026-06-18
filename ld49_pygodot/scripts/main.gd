@onready var status_label := $Shell/VBox/ScorePanel/StatusLabel
@onready var score_label := $Shell/VBox/ScorePanel/ScoreLabel
@onready var turn_label := $Shell/VBox/ScorePanel/TurnLabel
@onready var map_grid := $Shell/VBox/GameBody/MapGrid
@onready var units_panel := $Shell/VBox/GameBody/SidePanel/UnitsPanel

func _ready() -> void:
    GameState.reset()
    AudioManager.play_cue("main_ready")
    _connect_tiles()
    _refresh_units()
    _refresh_tiles()
    _refresh_runtime_labels()

func _on_intro_pressed() -> void:
    AudioManager.play_cue("open_intro")
    SceneChanger.go_to_intro()

func _on_fader_pressed() -> void:
    AudioManager.play_cue("open_fader")
    SceneChanger.show_fader()

func _on_reset_pressed() -> void:
    GameState.reset()
    _reset_tiles()
    _refresh_units()
    _refresh_tiles()
    AudioManager.stop_music()
    _refresh_runtime_labels()

func _on_advance_units_pressed() -> void:
    status_label.text = GameState.advance_units()
    GameState.next_turn()
    AudioManager.play_cue("units_move")
    _refresh_units()
    _refresh_tiles()
    score_label.text = GameState.describe_score()
    turn_label.text = GameState.describe_turn()

func _on_tile_spell_dropped(tile_id: String, spell_id: String, display_name: String) -> void:
    var summary := GameState.apply_spell(tile_id, spell_id)
    GameState.next_turn()
    AudioManager.play_cue("cast_%s" % spell_id)
    _refresh_units()
    _refresh_tiles()
    status_label.text = "%s cast on %s. %s" % [display_name, tile_id, summary]
    score_label.text = GameState.describe_score()
    turn_label.text = GameState.describe_turn()

func _connect_tiles() -> void:
    for tile in map_grid.get_children():
        if tile.has_signal("spell_dropped") and not tile.spell_dropped.is_connected(_on_tile_spell_dropped):
            tile.spell_dropped.connect(_on_tile_spell_dropped)

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

func _refresh_units() -> void:
    var unit_by_id := {}
    for unit in GameState.list_units():
        unit_by_id[unit["unit_id"]] = unit
    for unit_card in units_panel.get_children():
        if unit_card.has_method("apply_state") and unit_by_id.has(unit_card.unit_id):
            unit_card.apply_state(unit_by_id[unit_card.unit_id])

func _refresh_runtime_labels() -> void:
    status_label.text = "%s. %s. %s" % [
        GameState.describe_state(),
        GameState.describe_matrix(),
        AudioManager.describe_state(),
    ]
    score_label.text = GameState.describe_score()
    turn_label.text = GameState.describe_turn()
