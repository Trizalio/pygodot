from __future__ import annotations

import os
from pathlib import Path

from pygodot import Game, Node2D, Scene, Script, Vec2

ROOT = Path(__file__).parent

SNAKE_SCRIPT = Script(
    path="res://scripts/snake.gd",
    extends="Node2D",
    body="""
    const GRID_SIZE := Vector2i(24, 18)
    const CELL_SIZE := 28
    const TICK_SECONDS := 0.14

    var snake: Array[Vector2i] = []
    var direction := Vector2i.RIGHT
    var pending_direction := Vector2i.RIGHT
    var food := Vector2i.ZERO
    var score := 0
    var game_over := false
    var tick_accumulator := 0.0

    func _ready() -> void:
        reset_game()

    func _process(delta: float) -> void:
        read_input()
        if Input.is_action_just_pressed("restart"):
            reset_game()

        if game_over:
            queue_redraw()
            return

        tick_accumulator += delta
        while tick_accumulator >= TICK_SECONDS:
            tick_accumulator -= TICK_SECONDS
            step_game()

        queue_redraw()

    func read_input() -> void:
        if Input.is_action_just_pressed("move_up") and direction != Vector2i.DOWN:
            pending_direction = Vector2i.UP
        elif Input.is_action_just_pressed("move_down") and direction != Vector2i.UP:
            pending_direction = Vector2i.DOWN
        elif Input.is_action_just_pressed("move_left") and direction != Vector2i.RIGHT:
            pending_direction = Vector2i.LEFT
        elif Input.is_action_just_pressed("move_right") and direction != Vector2i.LEFT:
            pending_direction = Vector2i.RIGHT

    func reset_game() -> void:
        snake = [
            Vector2i(8, 9),
            Vector2i(7, 9),
            Vector2i(6, 9),
        ]
        direction = Vector2i.RIGHT
        pending_direction = Vector2i.RIGHT
        score = 0
        game_over = false
        tick_accumulator = 0.0
        place_food()
        queue_redraw()

    func step_game() -> void:
        direction = pending_direction
        var next_head := snake[0] + direction

        if is_wall(next_head) or next_head in snake:
            game_over = true
            return

        snake.insert(0, next_head)
        if next_head == food:
            score += 1
            place_food()
        else:
            snake.pop_back()

    func place_food() -> void:
        for y in range(GRID_SIZE.y):
            for x in range(GRID_SIZE.x):
                var candidate := Vector2i(
                    int(posmod(x * 7 + score * 5 + 3, GRID_SIZE.x)),
                    int(posmod(y * 5 + score * 3 + 2, GRID_SIZE.y))
                )
                if candidate not in snake:
                    food = candidate
                    return

        food = Vector2i(-1, -1)

    func is_wall(cell: Vector2i) -> bool:
        return cell.x < 0 or cell.y < 0 or cell.x >= GRID_SIZE.x or cell.y >= GRID_SIZE.y

    func _draw() -> void:
        draw_rect(Rect2(Vector2.ZERO, Vector2(GRID_SIZE * CELL_SIZE)), Color(0.04, 0.05, 0.06), true)
        draw_grid()
        draw_cell(food, Color(1.0, 0.35, 0.35))

        for index in range(snake.size()):
            var color: Color = Color(0.45, 1.0, 0.58) if index == 0 else Color(0.18, 0.74, 0.35)
            draw_cell(snake[index], color)

        draw_string(ThemeDB.fallback_font, Vector2(12, GRID_SIZE.y * CELL_SIZE + 28), "Score: %s" % score)
        if game_over:
            draw_string(
                ThemeDB.fallback_font,
                Vector2(220, GRID_SIZE.y * CELL_SIZE + 28),
                "Game over - press Space"
            )

    func draw_grid() -> void:
        var grid_color := Color(0.12, 0.14, 0.16)
        for x in range(GRID_SIZE.x + 1):
            var px := float(x * CELL_SIZE)
            draw_line(Vector2(px, 0), Vector2(px, GRID_SIZE.y * CELL_SIZE), grid_color)
        for y in range(GRID_SIZE.y + 1):
            var py := float(y * CELL_SIZE)
            draw_line(Vector2(0, py), Vector2(GRID_SIZE.x * CELL_SIZE, py), grid_color)

    func draw_cell(cell: Vector2i, color: Color) -> void:
        var position := Vector2(cell * CELL_SIZE) + Vector2(2, 2)
        var size := Vector2(CELL_SIZE - 4, CELL_SIZE - 4)
        draw_rect(Rect2(position, size), color, true)
    """,
)

game = Game(
    name="PygodotSnake",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/snake.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)

game.add_input_action("move_up", keys=["W", "UP"])
game.add_input_action("move_down", keys=["S", "DOWN"])
game.add_input_action("move_left", keys=["A", "LEFT"])
game.add_input_action("move_right", keys=["D", "RIGHT"])
game.add_input_action("restart", keys=["SPACE"])
game.set_window(size=Vec2(672, 560))

game.add_scene(
    Scene(
        path="res://scenes/snake.tscn",
        root=Node2D("Snake", script=SNAKE_SCRIPT),
    )
)

if __name__ == "__main__":
    game.run()
