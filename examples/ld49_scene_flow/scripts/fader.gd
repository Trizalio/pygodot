@onready var status_label := $Panel/VBox/StatusLabel

func _ready() -> void:
    AudioManager.play_cue("fader")
    status_label.text = "Minimal fader scene placeholder"

func _on_done_pressed() -> void:
    SceneChanger.go_to_menu()
