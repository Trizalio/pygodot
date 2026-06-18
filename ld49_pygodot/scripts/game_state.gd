extends Node

var port_stage := "runtime"
var last_event := ""
var turn := 1
var score := 0
var last_spell_id := ""
var last_cell_id := ""

func reset() -> void:
    Matrix.reset(5, 5)
    Rand.set_seed(4900)
    turn = 1
    score = 0
    last_event = "reset"
    last_spell_id = ""
    last_cell_id = ""

func apply_spell(cell_id: String, spell_id: String) -> String:
    if not Matrix.is_valid_cell(cell_id):
        last_event = "invalid:%s" % cell_id
        return last_event
    last_cell_id = cell_id
    last_spell_id = spell_id
    score += 10
    Matrix.set_cell(cell_id, {"spell_id": spell_id, "turn": turn})
    last_event = Utils.describe_spell_drop(spell_id, cell_id)
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
