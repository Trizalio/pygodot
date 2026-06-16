var selected_action := ""

@onready var status_label := $Panel/VBox/StatusLabel

func _ready() -> void:
    AudioManager.play_cue("menu")
    status_label.text = "SceneChanger and AudioManager are autoloaded"

func _on_start_pressed() -> void:
    selected_action = "intro"
    AudioManager.play_cue("start")
    SceneChanger.go_to_intro()

func _on_fader_pressed() -> void:
    selected_action = "fader"
    AudioManager.play_cue("fader")
    SceneChanger.show_fader()
