@export var spell_id := "spark"
@export var display_name := "Spark"

@onready var title := $Panel/Title

func _ready() -> void:
    title.text = display_name

func _get_drag_data(_at_position: Vector2) -> Variant:
    var preview := Label.new()
    preview.text = display_name
    set_drag_preview(preview)
    return {
        "type": "spell",
        "spell_id": spell_id,
        "display_name": display_name,
    }
