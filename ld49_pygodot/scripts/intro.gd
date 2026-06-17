@onready var status_label := $Panel/VBox/StatusLabel

func _ready() -> void:
    GameState.last_event = "intro"
    AudioManager.play_cue("intro")
    status_label.text = "%s. %s" % [GameState.describe_state(), AudioManager.describe_state()]

func _on_back_pressed() -> void:
    SceneChanger.go_to_main()
