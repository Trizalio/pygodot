@onready var log_label := $Panel/VBox/LogLabel

var drop_count := 0

func _ready() -> void:
    log_label.text = "Drop a spell onto a tile"

func _on_tile_spell_dropped(tile_id: String, _spell_id: String, display_name: String) -> void:
    drop_count += 1
    log_label.text = "%s on %s (%d)" % [display_name, tile_id, drop_count]
