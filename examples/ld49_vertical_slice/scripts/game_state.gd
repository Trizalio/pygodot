extends Node

var drop_count := 0
var last_spell_id := ""
var last_tile_id := ""

func reset() -> void:
    drop_count = 0
    last_spell_id = ""
    last_tile_id = ""

func apply_spell(tile_id: String, spell_id: String) -> String:
    drop_count += 1
    last_spell_id = spell_id
    last_tile_id = tile_id
    return "%s -> %s (%d)" % [spell_id, tile_id, drop_count]
