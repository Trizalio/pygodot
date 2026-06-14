func _on_play_button_pressed() -> void:
    $Status.text = "playing"
    $Player.play()

func _on_player_finished() -> void:
    $Status.text = "finished"
