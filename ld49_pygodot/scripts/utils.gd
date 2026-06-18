extends Node

func format_cell(cell_id: String) -> String:
    if cell_id.is_empty():
        return "none"
    return cell_id

func describe_spell_drop(spell_id: String, cell_id: String) -> String:
    return "%s -> %s" % [spell_id, format_cell(cell_id)]

func join_ids(values: Array[String]) -> String:
    var parts := PackedStringArray()
    for value in values:
        parts.append(value)
    return ", ".join(parts)
