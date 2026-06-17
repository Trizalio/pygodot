@export var unit_name := "Scout"

@onready var title := $Panel/VBox/Title
@onready var portrait := $Panel/VBox/Portrait

func _ready() -> void:
    title.text = unit_name

func play_feedback() -> void:
    portrait.modulate = Color(1.0, 0.55, 0.55, 1.0)
    var tween := create_tween()
    tween.tween_property(portrait, "modulate", Color.WHITE, 0.4)
