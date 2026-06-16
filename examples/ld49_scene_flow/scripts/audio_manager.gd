extends Node

var last_cue := ""

func play_cue(name: String) -> void:
    last_cue = name

func stop_music() -> void:
    last_cue = "stopped"
