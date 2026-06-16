@onready var status_label := $Panel/VBox/StatusLabel

func _ready() -> void:
    AudioManager.play_cue("intro")
    status_label.text = "Intro scene reached through SceneChanger"

func _on_back_pressed() -> void:
    AudioManager.play_cue("menu")
    SceneChanger.go_to_menu()
