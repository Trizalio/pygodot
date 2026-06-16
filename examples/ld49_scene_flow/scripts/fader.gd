@onready var status_label := $Panel/VBox/StatusLabel

func _ready() -> void:
    AudioManager.play_cue("fader")
    status_label.text = "Minimal fader placeholder. %s" % AudioManager.describe_state()

func _on_done_pressed() -> void:
    AudioManager.play_cue("menu")
    status_label.text = "Fader done. %s" % AudioManager.describe_state()
    SceneChanger.go_to_menu()
