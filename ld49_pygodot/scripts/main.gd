@onready var status_label := $Shell/VBox/ScorePanel/StatusLabel
@onready var score_label := $Shell/VBox/ScorePanel/ScoreLabel
@onready var turn_label := $Shell/VBox/ScorePanel/TurnLabel

func _ready() -> void:
    GameState.reset()
    AudioManager.play_cue("main_ready")
    _refresh_runtime_labels()

func _on_intro_pressed() -> void:
    AudioManager.play_cue("open_intro")
    SceneChanger.go_to_intro()

func _on_fader_pressed() -> void:
    AudioManager.play_cue("open_fader")
    SceneChanger.show_fader()

func _on_reset_pressed() -> void:
    GameState.reset()
    AudioManager.stop_music()
    _refresh_runtime_labels()

func _refresh_runtime_labels() -> void:
    status_label.text = "%s. %s. %s" % [
        GameState.describe_state(),
        GameState.describe_matrix(),
        AudioManager.describe_state(),
    ]
    score_label.text = GameState.describe_score()
    turn_label.text = GameState.describe_turn()
