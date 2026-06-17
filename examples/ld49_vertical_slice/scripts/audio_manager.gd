extends Node

var last_cue := ""

func play_cue(name: String) -> void:
    last_cue = name

func describe_state() -> String:
    if last_cue.is_empty():
        return "Audio cue: none"
    return "Audio cue: %s" % last_cue
