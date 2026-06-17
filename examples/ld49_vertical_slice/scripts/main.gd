@onready var log_label := $Panel/VBox/Header/LogLabel
@onready var unit := $Panel/VBox/BoardRow/UnitColumn/UnitScout

func _ready() -> void:
    log_label.text = "Drag Spark onto any tile"
    AudioManager.play_cue("battle_ready")

func _on_tile_spell_dropped(tile_id: String, spell_id: String, display_name: String) -> void:
    var summary := GameState.apply_spell(tile_id, spell_id)
    AudioManager.play_cue("spell_drop")
    log_label.text = "%s on %s. %s" % [display_name, tile_id, summary]
    unit.play_feedback()

func _on_back_pressed() -> void:
    SceneChanger.go_to_menu()
