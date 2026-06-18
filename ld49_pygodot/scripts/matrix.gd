extends Node

var width := 5
var height := 5
var cells: Dictionary = {}

func reset(new_width: int = 5, new_height: int = 5) -> void:
    width = new_width
    height = new_height
    cells.clear()

func is_valid_cell(cell_id: String) -> bool:
    if cell_id.length() < 2:
        return false
    var row := cell_id.substr(0, 1)
    var column := int(cell_id.substr(1))
    var row_index := row.unicode_at(0) - "A".unicode_at(0)
    return row_index >= 0 and row_index < height and column >= 1 and column <= width

func set_cell(cell_id: String, value: Variant) -> void:
    if not is_valid_cell(cell_id):
        push_warning("Ignoring invalid matrix cell: %s" % cell_id)
        return
    cells[cell_id] = value

func get_cell(cell_id: String, fallback: Variant = null) -> Variant:
    return cells.get(cell_id, fallback)

func clear_cell(cell_id: String) -> void:
    cells.erase(cell_id)

func occupied_count() -> int:
    return cells.size()
