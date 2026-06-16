@onready var status_label := $Panel/VBox/StatusLabel

func _ready() -> void:
    AudioManager.play_cue("intro")
    status_label.text = "Intro reached through SceneChanger. %s" % AudioManager.describe_state()

func _on_back_pressed() -> void:
    AudioManager.play_cue("menu")
    status_label.text = "Returning to menu. %s" % AudioManager.describe_state()
    SceneChanger.go_to_menu()
