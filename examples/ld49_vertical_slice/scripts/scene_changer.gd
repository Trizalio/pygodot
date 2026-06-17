extends Node

const MENU_SCENE := "res://scenes/menu.tscn"
const BATTLE_SCENE := "res://scenes/main.tscn"

var last_requested_scene := MENU_SCENE

func go_to_menu() -> void:
    change_scene(MENU_SCENE)

func go_to_battle() -> void:
    change_scene(BATTLE_SCENE)

func change_scene(path: String) -> void:
    last_requested_scene = path
    get_tree().change_scene_to_file(path)
