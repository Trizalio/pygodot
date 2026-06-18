extends Node

var port_stage := "runtime"
var last_event := ""
var turn := 1
var score := 0
var last_spell_id := ""
var last_cell_id := ""
var units: Dictionary = {}
var castle_capacity := 6
var castle_counts := {"demon": 0, "undead": 0, "greenskin": 0}
var spawn_index := 0

func reset() -> void:
    Matrix.reset(5, 5)
    Rand.set_seed(4900)
    turn = 1
    score = 0
    last_event = "reset"
    last_spell_id = ""
    last_cell_id = ""
    castle_counts = {"demon": 0, "undead": 0, "greenskin": 0}
    spawn_index = 0
    units = {
        "imp": _make_unit("imp", "Imp", "demon", "B1", 4),
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
    var affected: Array[String] = []
    for target_cell in _target_cells_for_spell(cell_id, spell_id):
        var effect := _apply_spell_to_cell(target_cell, spell_id)
        if not effect.is_empty():
            affected.append(effect)
    if affected.is_empty():
        last_event = Utils.describe_spell_drop(spell_id, cell_id)
        return last_event
    last_event = "; ".join(affected)
    return last_event

func resolve_turn() -> String:
    var traits := _resolve_neighbor_traits()
    var moved := _move_units()
    var spawned := _spawn_wave()
    turn += 1
    if traits.is_empty():
        last_event = "%s; %s" % [moved, spawned]
    else:
        last_event = "%s; %s; %s" % [traits, moved, spawned]
    return last_event

func advance_units() -> String:
    return resolve_turn()

func _move_units() -> String:
    var moved := PackedStringArray()
    for unit_id in units.keys():
        var unit: Dictionary = units[unit_id]
        var status := str(unit.get("status", ""))
        if status == "defeated":
            continue
        var tick_result: String = _tick_status(unit_id)
        unit = units[unit_id]
        if str(unit.get("status", "")) == "defeated":
            moved.append(tick_result)
            continue
        if tick_result.ends_with(":frozen"):
            moved.append(tick_result)
            continue
        var from_cell := str(unit["cell_id"])
        var to_cell: String = _next_cell(from_cell)
        if to_cell == "CASTLE":
            _exit_matrix(unit_id)
            var faction := str(unit["faction"])
            castle_counts[faction] = int(castle_counts.get(faction, 0)) + 1
            moved.append("%s reached castle" % unit["display_name"])
            units.erase(unit_id)
            continue
        var blocker_id := _unit_id_at(to_cell)
        if not blocker_id.is_empty():
            moved.append(_clash_units(unit_id, blocker_id, to_cell))
            continue
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

func describe_castle() -> String:
    return "Castle %d/%d D:%d U:%d G:%d" % [
        _castle_total(),
        castle_capacity,
        int(castle_counts.get("demon", 0)),
        int(castle_counts.get("undead", 0)),
        int(castle_counts.get("greenskin", 0)),
    ]

func describe_matrix() -> String:
    return "%d occupied / %d cells" % [Matrix.occupied_count(), Matrix.width * Matrix.height]

func is_complete() -> bool:
    return _castle_total() >= castle_capacity

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

func _target_cells_for_spell(cell_id: String, spell_id: String) -> Array[String]:
    var cells: Array[String] = [cell_id]
    if spell_id == "fireball" or spell_id == "frost":
        for neighbor in MatrixUtils.neighbors(cell_id, Matrix.width, Matrix.height):
            cells.append(neighbor)
    if spell_id == "shield" or spell_id == "heal":
        var anchor_id := _unit_id_at(cell_id)
        if not anchor_id.is_empty():
            var anchor: Dictionary = units[anchor_id]
            var faction := str(anchor["faction"])
            for neighbor in MatrixUtils.neighbors(cell_id, Matrix.width, Matrix.height):
                var neighbor_id := _unit_id_at(neighbor)
                if neighbor_id.is_empty():
                    continue
                var neighbor_unit: Dictionary = units[neighbor_id]
                if str(neighbor_unit["faction"]) == faction:
                    cells.append(neighbor)
    return cells

func _apply_spell_to_cell(cell_id: String, spell_id: String) -> String:
    var target_id := _unit_id_at(cell_id)
    if target_id.is_empty():
        return ""
    return _apply_spell_to_unit(target_id, spell_id, cell_id)

func _make_unit(unit_id: String, display_name: String, faction: String, cell_id: String, hp: int) -> Dictionary:
    return {
        "unit_id": unit_id,
        "display_name": display_name,
        "faction": faction,
        "cell_id": cell_id,
        "hp": hp,
        "max_hp": hp,
        "shield": 0,
        "status": "ready",
    }

func _apply_spell_to_unit(unit_id: String, spell_id: String, cell_id: String) -> String:
    var unit: Dictionary = units[unit_id]
    match spell_id:
        "fireball":
            _damage_unit(unit, 2)
            unit["status"] = "burning"
        "frost":
            _damage_unit(unit, 1)
            unit["status"] = "frozen"
        "shield":
            unit["shield"] = int(unit.get("shield", 0)) + 2
            unit["status"] = "shielded"
        "heal":
            unit["hp"] = min(int(unit.get("max_hp", unit["hp"])), int(unit["hp"]) + 2)
            unit["status"] = "healed"
        _:
            _damage_unit(unit, 1)
            unit["status"] = "hit"
    if int(unit["hp"]) <= 0:
        unit["hp"] = 0
        unit["status"] = "defeated"
        units[unit_id] = unit
        _exit_matrix(unit_id)
        score += 15
        return "%s defeated %s at %s" % [spell_id, unit["display_name"], cell_id]
    units[unit_id] = unit
    return "%s affected %s at %s" % [spell_id, unit["display_name"], cell_id]

func _spawn_wave() -> String:
    if is_complete():
        return "castle full"
    var spawn_count := 1
    if turn % 2 == 0:
        spawn_count = 2
    var spawned := PackedStringArray()
    for index in range(spawn_count):
        var cell_id := _next_spawn_cell()
        if cell_id.is_empty():
            continue
        var faction := _spawn_faction()
        var unit_id := "spawn_%d" % spawn_index
        spawn_index += 1
        var display_name := _spawn_name(faction)
        units[unit_id] = _make_unit(unit_id, display_name, faction, cell_id, _spawn_hp(faction))
        _enter_matrix(unit_id)
        spawned.append("%s@%s" % [display_name, cell_id])
    if spawned.is_empty():
        return "no spawn room"
    return "spawned %s" % ", ".join(spawned)

func _next_spawn_cell() -> String:
    for offset in range(Matrix.width):
        var column := ((spawn_index + offset) % Matrix.width) + 1
        var cell_id := "E%d" % column
        if _unit_id_at(cell_id).is_empty():
            return cell_id
    return ""

func _spawn_faction() -> String:
    match spawn_index % 3:
        0:
            return "demon"
        1:
            return "undead"
        _:
            return "greenskin"

func _spawn_name(faction: String) -> String:
    match faction:
        "demon":
            return "Imp"
        "undead":
            return "Bones"
        _:
            return "Gob"

func _spawn_hp(faction: String) -> int:
    match faction:
        "undead":
            return 5
        "greenskin":
            return 3
        _:
            return 4

func _tick_status(unit_id: String) -> String:
    var unit: Dictionary = units[unit_id]
    var status := str(unit.get("status", "ready"))
    if status == "burning":
        _damage_unit(unit, 1)
        if int(unit["hp"]) <= 0:
            unit["hp"] = 0
            unit["status"] = "defeated"
            units[unit_id] = unit
            _exit_matrix(unit_id)
            score += 15
            return "%s:burned-out" % unit["display_name"]
        unit["status"] = "ready"
        units[unit_id] = unit
        return "%s:burn-tick" % unit["display_name"]
    if status == "frozen":
        unit["status"] = "ready"
        units[unit_id] = unit
        return "%s:frozen" % unit["display_name"]
    if [
        "shielded",
        "healed",
        "moving",
        "blocked",
        "clash",
        "scorched",
        "horde",
        "braced",
        "stacked",
        "raging",
    ].has(status):
        unit["status"] = "ready"
        units[unit_id] = unit
    return ""

func _damage_unit(unit: Dictionary, amount: int) -> void:
    var shield: int = int(unit.get("shield", 0))
    var remaining := amount
    if shield > 0:
        var absorbed: int = min(shield, remaining)
        shield -= absorbed
        remaining -= absorbed
    unit["shield"] = shield
    if remaining > 0:
        unit["hp"] = int(unit["hp"]) - remaining

func _enter_matrix(unit_id: String) -> void:
    var unit: Dictionary = units[unit_id]
    var cell_id := str(unit["cell_id"])
    var cell: Dictionary = Matrix.get_cell(cell_id, {})
    cell["unit_id"] = unit_id
    Matrix.set_cell(cell_id, cell)

func _unit_id_at(cell_id: String) -> String:
    var cell: Dictionary = Matrix.get_cell(cell_id, {})
    return str(cell.get("unit_id", ""))

func _clash_units(attacker_id: String, blocker_id: String, cell_id: String) -> String:
    var attacker: Dictionary = units[attacker_id]
    var blocker: Dictionary = units[blocker_id]
    var attacker_faction := str(attacker["faction"])
    var blocker_faction := str(blocker["faction"])
    if attacker_faction == blocker_faction:
        attacker["status"] = "stacked"
        blocker["status"] = "stacked"
        units[attacker_id] = attacker
        units[blocker_id] = blocker
        return "%s stacked behind %s at %s" % [attacker["display_name"], blocker["display_name"], cell_id]
    var attacker_damage := 1
    var blocker_damage := 1
    if attacker_faction == "demon":
        blocker_damage += 1
        attacker["status"] = "raging"
    else:
        attacker["status"] = "blocked"
    if blocker_faction == "undead":
        blocker["shield"] = int(blocker.get("shield", 0)) + 1
    if attacker_faction == "greenskin":
        blocker_damage += 1
        attacker_damage += 1
        attacker["status"] = "raging"
    _damage_unit(attacker, attacker_damage)
    _damage_unit(blocker, blocker_damage)
    if blocker_faction == "undead":
        blocker["status"] = "braced"
    else:
        blocker["status"] = "clash"
    units[attacker_id] = attacker
    units[blocker_id] = blocker
    if int(attacker["hp"]) <= 0:
        attacker["status"] = "defeated"
        units[attacker_id] = attacker
        _exit_matrix(attacker_id)
    if int(blocker["hp"]) <= 0:
        blocker["status"] = "defeated"
        units[blocker_id] = blocker
        _exit_matrix(blocker_id)
    return "%s blocked by %s at %s" % [attacker["display_name"], blocker["display_name"], cell_id]

func _resolve_neighbor_traits() -> String:
    var events := PackedStringArray()
    for unit_id in units.keys():
        if not units.has(unit_id):
            continue
        var unit: Dictionary = units[unit_id]
        if str(unit.get("status", "")) == "defeated":
            continue
        var faction := str(unit["faction"])
        var cell_id := str(unit["cell_id"])
        var neighbors := _neighbor_unit_ids(cell_id)
        if faction == "demon":
            for neighbor_id in neighbors:
                if not units.has(neighbor_id):
                    continue
                var neighbor: Dictionary = units[neighbor_id]
                if str(neighbor["faction"]) == faction:
                    continue
                _damage_unit(neighbor, 1)
                if int(neighbor["hp"]) <= 0:
                    _defeat_unit(neighbor_id, neighbor)
                    events.append("%s scorched %s" % [unit["display_name"], neighbor["display_name"]])
                else:
                    neighbor["status"] = "scorched"
                    units[neighbor_id] = neighbor
                    events.append("%s scorched %s" % [unit["display_name"], neighbor["display_name"]])
        elif faction == "undead":
            if _has_neighbor_faction(neighbors, "undead"):
                var old_hp := int(unit["hp"])
                unit["hp"] = min(int(unit["max_hp"]), old_hp + 1)
                unit["status"] = "horde"
                units[unit_id] = unit
                if int(unit["hp"]) > old_hp:
                    events.append("%s horde healed" % unit["display_name"])
        elif faction == "greenskin":
            if _has_enemy_neighbor(neighbors, faction):
                unit["shield"] = int(unit.get("shield", 0)) + 1
                unit["status"] = "braced"
                units[unit_id] = unit
                events.append("%s braced" % unit["display_name"])
    if events.is_empty():
        return ""
    return "neighbors %s" % ", ".join(events)

func _neighbor_unit_ids(cell_id: String) -> Array[String]:
    var result: Array[String] = []
    for neighbor in MatrixUtils.neighbors(cell_id, Matrix.width, Matrix.height):
        var unit_id := _unit_id_at(neighbor)
        if not unit_id.is_empty():
            result.append(unit_id)
    return result

func _has_neighbor_faction(unit_ids: Array[String], faction: String) -> bool:
    for unit_id in unit_ids:
        if units.has(unit_id) and str(units[unit_id]["faction"]) == faction:
            return true
    return false

func _has_enemy_neighbor(unit_ids: Array[String], faction: String) -> bool:
    for unit_id in unit_ids:
        if units.has(unit_id) and str(units[unit_id]["faction"]) != faction:
            return true
    return false

func _defeat_unit(unit_id: String, unit: Dictionary) -> void:
    unit["hp"] = 0
    unit["status"] = "defeated"
    units[unit_id] = unit
    _exit_matrix(unit_id)
    score += 15

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
    var row_index := row.unicode_at(0) - "A".unicode_at(0)
    if row_index <= 0:
        return "CASTLE"
    return "%s%d" % [String.chr("A".unicode_at(0) + row_index - 1), column]

func _castle_total() -> int:
    return int(castle_counts.get("demon", 0)) + int(castle_counts.get("undead", 0)) + int(castle_counts.get("greenskin", 0))
