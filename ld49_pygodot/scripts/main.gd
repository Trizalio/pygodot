@onready var status_label := $Panel/VBox/StatusLabel

func _ready() -> void:
    GameState.reset()
    AudioManager.play_cue("main_ready")
    status_label.text = "%s. %s" % [GameState.describe_state(), AudioManager.describe_state()]

func _on_intro_pressed() -> void:
    AudioManager.play_cue("open_intro")
    SceneChanger.go_to_intro()

func _on_fader_pressed() -> void:
    AudioManager.play_cue("open_fader")
    SceneChanger.show_fader()
