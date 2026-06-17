signal spell_dropped(tile_id: String, spell_id: String, display_name: String)

@export var tile_id := "A1"

@onready var panel := $Panel
@onready var title := $Panel/VBox/Title
@onready var state := $Panel/VBox/State

func _ready() -> void:
    title.text = tile_id
    state.text = "Empty"

func _can_drop_data(_at_position: Vector2, data: Variant) -> bool:
    return data is Dictionary and data.get("type") == "spell"

func _drop_data(_at_position: Vector2, data: Variant) -> void:
    var spell_id := str(data.get("spell_id", "unknown"))
    var display_name := str(data.get("display_name", spell_id))
    state.text = display_name
    _flash()
    spell_dropped.emit(tile_id, spell_id, display_name)

func _flash() -> void:
    panel.modulate = Color(1.0, 0.85, 0.35, 1.0)
    var tween := create_tween()
    tween.tween_property(panel, "modulate", Color.WHITE, 0.35)
