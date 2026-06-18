extends Node

func cell_id(row: int, column: int) -> String:
    return "%s%d" % [String.chr("A".unicode_at(0) + row), column + 1]

func all_cells(width: int, height: int) -> Array[String]:
    var result: Array[String] = []
    for row in range(height):
        for column in range(width):
            result.append(cell_id(row, column))
    return result

func neighbors(cell: String, width: int, height: int) -> Array[String]:
    var result: Array[String] = []
    var row: int = cell.substr(0, 1).unicode_at(0) - "A".unicode_at(0)
    var column: int = int(cell.substr(1)) - 1
    for offset in [Vector2i(0, -1), Vector2i(1, 0), Vector2i(0, 1), Vector2i(-1, 0)]:
        var next_row: int = row + offset.y
        var next_column: int = column + offset.x
        if next_row >= 0 and next_row < height and next_column >= 0 and next_column < width:
            result.append(cell_id(next_row, next_column))
    return result

func manhattan_distance(a: String, b: String) -> int:
    var row_a: int = a.substr(0, 1).unicode_at(0) - "A".unicode_at(0)
    var column_a: int = int(a.substr(1)) - 1
    var row_b: int = b.substr(0, 1).unicode_at(0) - "A".unicode_at(0)
    var column_b: int = int(b.substr(1)) - 1
    return abs(row_a - row_b) + abs(column_a - column_b)
