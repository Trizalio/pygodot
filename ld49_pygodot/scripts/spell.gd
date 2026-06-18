@export var spell_id := "fireball"
@export var display_name := "Fireball"

@onready var title := $VBox/Title
@onready var hint := $VBox/Hint

func _ready() -> void:
    title.text = display_name
    hint.text = "drag to tile"

func _get_drag_data(_at_position: Vector2) -> Variant:
    var preview := Label.new()
    preview.text = display_name
    set_drag_preview(preview)
    return {
        "type": "spell",
        "spell_id": spell_id,
        "display_name": display_name,
    }
