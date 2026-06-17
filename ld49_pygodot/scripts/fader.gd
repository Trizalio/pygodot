@onready var overlay := $Panel/VBox/FadePreview
@onready var status_label := $Panel/VBox/StatusLabel

func _ready() -> void:
    GameState.last_event = "fader"
    AudioManager.play_cue("fader")
    status_label.text = "%s. %s" % [GameState.describe_state(), AudioManager.describe_state()]
    var tween := create_tween()
    overlay.modulate = Color(1, 1, 1, 0.25)
    tween.tween_property(overlay, "modulate", Color(1, 1, 1, 0.8), 0.5)

func _on_done_pressed() -> void:
    SceneChanger.go_to_main()
