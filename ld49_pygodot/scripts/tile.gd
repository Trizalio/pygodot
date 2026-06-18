signal spell_dropped(tile_id: String, spell_id: String, display_name: String)

@export var tile_id := "A1"

@onready var title := $VBox/Label
@onready var state := $VBox/State

func _ready() -> void:
    title.text = tile_id
    state.text = "Empty"

func _can_drop_data(_at_position: Vector2, data: Variant) -> bool:
    var can_drop: bool = data is Dictionary and data.get("type") == "spell"
    if can_drop:
        modulate = Color(1.0, 0.85, 0.35, 1.0)
    return can_drop

func _drop_data(_at_position: Vector2, data: Variant) -> void:
    var spell_id := str(data.get("spell_id", "unknown"))
    var display_name := str(data.get("display_name", spell_id))
    state.text = display_name
    _flash(Color(1.0, 0.45, 0.25, 1.0))
    spell_dropped.emit(tile_id, spell_id, display_name)

func _notification(what: int) -> void:
    if what == NOTIFICATION_DRAG_END:
        _flash(Color.WHITE)

func _flash(color: Color) -> void:
    modulate = color
    var tween := create_tween()
    tween.tween_property(self, "modulate", Color.WHITE, 0.35)
