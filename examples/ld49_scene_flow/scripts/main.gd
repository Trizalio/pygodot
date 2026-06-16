var selected_action := ""

@onready var status_label := $Panel/VBox/StatusLabel

func _ready() -> void:
    AudioManager.play_cue("menu")
    status_label.text = "Menu ready. %s" % AudioManager.describe_state()

func _on_start_pressed() -> void:
    selected_action = "intro"
    AudioManager.play_cue("start")
    status_label.text = "Start pressed. %s" % AudioManager.describe_state()
    SceneChanger.go_to_intro()

func _on_fader_pressed() -> void:
    selected_action = "fader"
    AudioManager.play_cue("fader")
    status_label.text = "Fader requested. %s" % AudioManager.describe_state()
    SceneChanger.show_fader()
