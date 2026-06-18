extends Node

var port_stage := "runtime"
var last_event := ""
var turn := 1
var score := 0
var last_spell_id := ""
var last_cell_id := ""
var units: Dictionary = {}

func reset() -> void:
    Matrix.reset(5, 5)
    Rand.set_seed(4900)
    turn = 1
    score = 0
    last_event = "reset"
    last_spell_id = ""
    last_cell_id = ""
    units = {
        "imp": _make_unit("imp", "Imp", "demon", "A1", 4),
        "bones": _make_unit("bones", "Bones", "undead", "C3", 5),
        "gob": _make_unit("gob", "Gob", "greenskin", "E1", 3),
    }
    for unit_id in units:
        _enter_matrix(unit_id)

func apply_spell(cell_id: String, spell_id: String) -> String:
    if not Matrix.is_valid_cell(cell_id):
        last_event = "invalid:%s" % cell_id
        return last_event
    last_cell_id = cell_id
    last_spell_id = spell_id
    score += 10
    var cell: Dictionary = Matrix.get_cell(cell_id, {})
    cell["spell_id"] = spell_id
    cell["turn"] = turn
    Matrix.set_cell(cell_id, cell)
    var target_id := str(cell.get("unit_id", ""))
    if target_id.is_empty():
        last_event = Utils.describe_spell_drop(spell_id, cell_id)
        return last_event
    var target: Dictionary = units[target_id]
    target["hp"] = int(target["hp"]) - 2
    target["status"] = "burning"
    if int(target["hp"]) <= 0:
        target["status"] = "defeated"
        _exit_matrix(target_id)
        score += 15
    units[target_id] = target
    last_event = "%s hit %s at %s" % [spell_id, target["display_name"], cell_id]
    return last_event

func advance_units() -> String:
    var moved := PackedStringArray()
    for unit_id in units:
        var unit: Dictionary = units[unit_id]
        if str(unit.get("status", "")) == "defeated":
            continue
        var from_cell := str(unit["cell_id"])
        var to_cell: String = _next_cell(from_cell)
        _exit_matrix(unit_id)
        unit["cell_id"] = to_cell
        unit["status"] = "moving"
        units[unit_id] = unit
        _enter_matrix(unit_id)
        moved.append("%s:%s->%s" % [unit["display_name"], from_cell, to_cell])
    if moved.is_empty():
        last_event = "no units moved"
    else:
        last_event = "moved %s" % ", ".join(moved)
    return last_event

func next_turn() -> void:
    turn += 1
    last_event = "turn:%d" % turn

func describe_state() -> String:
    if last_event.is_empty():
        return "LD49 runtime ready"
    return "LD49 runtime: %s" % last_event

func describe_score() -> String:
    return "Score %d" % score

func describe_turn() -> String:
    return "Turn %d" % turn

func describe_matrix() -> String:
    return "%d occupied / %d cells" % [Matrix.occupied_count(), Matrix.width * Matrix.height]

func list_units() -> Array:
    var result: Array = []
    for unit_id in units:
        result.append(units[unit_id].duplicate())
    return result

func unit_at(cell_id: String) -> Dictionary:
    var cell: Dictionary = Matrix.get_cell(cell_id, {})
    var unit_id := str(cell.get("unit_id", ""))
    if unit_id.is_empty():
        return {}
    return units.get(unit_id, {}).duplicate()

func _make_unit(unit_id: String, display_name: String, faction: String, cell_id: String, hp: int) -> Dictionary:
    return {
        "unit_id": unit_id,
        "display_name": display_name,
        "faction": faction,
        "cell_id": cell_id,
        "hp": hp,
        "status": "ready",
    }

func _enter_matrix(unit_id: String) -> void:
    var unit: Dictionary = units[unit_id]
    var cell_id := str(unit["cell_id"])
    var cell: Dictionary = Matrix.get_cell(cell_id, {})
    cell["unit_id"] = unit_id
    Matrix.set_cell(cell_id, cell)

func _exit_matrix(unit_id: String) -> void:
    var unit: Dictionary = units[unit_id]
    var cell_id := str(unit["cell_id"])
    var cell: Dictionary = Matrix.get_cell(cell_id, {})
    if str(cell.get("unit_id", "")) == unit_id:
        cell.erase("unit_id")
        if cell.is_empty():
            Matrix.clear_cell(cell_id)
        else:
            Matrix.set_cell(cell_id, cell)

func _next_cell(cell_id: String) -> String:
    var row := cell_id.substr(0, 1)
    var column := int(cell_id.substr(1))
    column += 1
    if column > Matrix.width:
        column = 1
    return "%s%d" % [row, column]
