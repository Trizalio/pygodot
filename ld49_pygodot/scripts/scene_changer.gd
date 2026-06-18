extends Node

const MAIN_SCENE := "res://scenes/main.tscn"
const INTRO_SCENE := "res://scenes/intro.tscn"
const FADER_SCENE := "res://scenes/fader.tscn"
const END_SCENE := "res://scenes/end.tscn"

var last_requested_scene := MAIN_SCENE

func go_to_main() -> void:
    change_scene(MAIN_SCENE)

func go_to_intro() -> void:
    change_scene(INTRO_SCENE)

func show_fader() -> void:
    change_scene(FADER_SCENE)

func go_to_end() -> void:
    change_scene(END_SCENE)

func change_scene(path: String) -> void:
    last_requested_scene = path
    get_tree().change_scene_to_file(path)
