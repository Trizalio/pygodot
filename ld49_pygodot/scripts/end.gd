@onready var status_label := $Panel/VBox/StatusLabel

func _ready() -> void:
    status_label.text = "%s. %s" % [
        GameState.describe_score(),
        GameState.describe_turn(),
    ]
    AudioManager.play_cue("battle_complete")

func _on_back_pressed() -> void:
    SceneChanger.go_to_main()
