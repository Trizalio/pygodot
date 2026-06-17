@onready var status_label := $Panel/VBox/StatusLabel

func _ready() -> void:
    GameState.reset()
    status_label.text = "Ready. %s" % AudioManager.describe_state()

func _on_start_pressed() -> void:
    AudioManager.play_cue("menu_start")
    SceneChanger.go_to_battle()
