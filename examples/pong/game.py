from __future__ import annotations

import os
from pathlib import Path

from pygodot import Button, Color, ColorRect, Control, Game, Label, Node2D, Scene, Script, Vec2, signal

ROOT = Path(__file__).parent

MENU_SCRIPT = Script(
    path="res://scripts/menu.gd",
    extends="Control",
    body="""
    func _on_start_pressed() -> void:
        get_tree().change_scene_to_file("res://scenes/pong.tscn")

    func _on_exit_pressed() -> void:
        get_tree().quit()
    """,
)

PONG_SCRIPT = Script(
    path="res://scripts/pong.gd",
    extends="Node2D",
    body="""
    const SCREEN_SIZE := Vector2(800, 600)
    const PADDLE_SIZE := Vector2(18, 96)
    const BALL_SIZE := Vector2(16, 16)
    const PADDLE_SPEED := 420.0
    const BALL_SPEED := 320.0

    var left_score := 0
    var right_score := 0
    var ball_velocity := Vector2.ZERO

    func _ready() -> void:
        reset_game()

    func _process(delta: float) -> void:
        if Input.is_action_just_pressed("restart"):
            reset_game()

        move_paddles(delta)
        move_ball(delta)
        update_scores()

    func reset_game() -> void:
        left_score = 0
        right_score = 0
        $LeftPaddle.position = Vector2(32, 252)
        $RightPaddle.position = Vector2(750, 252)
        reset_ball(1)
        update_scores()

    func move_paddles(delta: float) -> void:
        var left_direction := 0.0
        if Input.is_action_pressed("left_up"):
            left_direction -= 1.0
        if Input.is_action_pressed("left_down"):
            left_direction += 1.0

        var right_direction := 0.0
        if Input.is_action_pressed("right_up"):
            right_direction -= 1.0
        if Input.is_action_pressed("right_down"):
            right_direction += 1.0

        $LeftPaddle.position.y = clamp(
            $LeftPaddle.position.y + left_direction * PADDLE_SPEED * delta,
            0.0,
            SCREEN_SIZE.y - PADDLE_SIZE.y
        )
        $RightPaddle.position.y = clamp(
            $RightPaddle.position.y + right_direction * PADDLE_SPEED * delta,
            0.0,
            SCREEN_SIZE.y - PADDLE_SIZE.y
        )

    func move_ball(delta: float) -> void:
        $Ball.position += ball_velocity * delta
        bounce_from_walls()
        bounce_from_paddles()

        if $Ball.position.x + BALL_SIZE.x < 0.0:
            right_score += 1
            reset_ball(-1)
        elif $Ball.position.x > SCREEN_SIZE.x:
            left_score += 1
            reset_ball(1)

    func bounce_from_walls() -> void:
        if $Ball.position.y <= 0.0:
            $Ball.position.y = 0.0
            ball_velocity.y = abs(ball_velocity.y)
        elif $Ball.position.y + BALL_SIZE.y >= SCREEN_SIZE.y:
            $Ball.position.y = SCREEN_SIZE.y - BALL_SIZE.y
            ball_velocity.y = -abs(ball_velocity.y)

    func bounce_from_paddles() -> void:
        var ball_rect := Rect2($Ball.position, BALL_SIZE)
        var left_rect := Rect2($LeftPaddle.position, PADDLE_SIZE)
        var right_rect := Rect2($RightPaddle.position, PADDLE_SIZE)

        if ball_velocity.x < 0.0 and ball_rect.intersects(left_rect):
            $Ball.position.x = $LeftPaddle.position.x + PADDLE_SIZE.x
            ball_velocity.x = abs(ball_velocity.x)
            apply_paddle_spin($LeftPaddle.position.y)
        elif ball_velocity.x > 0.0 and ball_rect.intersects(right_rect):
            $Ball.position.x = $RightPaddle.position.x - BALL_SIZE.x
            ball_velocity.x = -abs(ball_velocity.x)
            apply_paddle_spin($RightPaddle.position.y)

    func apply_paddle_spin(paddle_y: float) -> void:
        var paddle_center: float = paddle_y + PADDLE_SIZE.y * 0.5
        var ball_center: float = $Ball.position.y + BALL_SIZE.y * 0.5
        var offset: float = clamp((ball_center - paddle_center) / (PADDLE_SIZE.y * 0.5), -1.0, 1.0)
        ball_velocity.y = offset * BALL_SPEED
        ball_velocity = ball_velocity.normalized() * BALL_SPEED

    func reset_ball(direction: int) -> void:
        $Ball.position = Vector2(392, 292)
        ball_velocity = Vector2(float(direction), 0.45).normalized() * BALL_SPEED

    func update_scores() -> void:
        $LeftScore.text = str(left_score)
        $RightScore.text = str(right_score)
    """,
)

game = Game(
    name="PygodotPong",
    source_root=ROOT,
    build_dir=ROOT / "build" / "godot_project",
    main_scene="res://scenes/menu.tscn",
    godot_bin=os.environ.get("GODOT_BIN", "godot"),
)

game.add_input_action("left_up", keys=["W"])
game.add_input_action("left_down", keys=["S"])
game.add_input_action("right_up", keys=["UP"])
game.add_input_action("right_down", keys=["DOWN"])
game.add_input_action("restart", keys=["SPACE"])

game.add_scene(
    Scene(
        path="res://scenes/menu.tscn",
        root=Control(
            "Menu",
            script=MENU_SCRIPT,
            children=[
                ColorRect(
                    "Background",
                    position=Vec2(0, 0),
                    size=Vec2(800, 600),
                    color=Color(0.03, 0.04, 0.05),
                ),
                Label(
                    "Title",
                    text="Pygodot Pong",
                    position=Vec2(310, 160),
                ),
                Button(
                    "StartButton",
                    text="Start",
                    position=Vec2(330, 260),
                    size=Vec2(140, 44),
                    signals=[
                        signal("pressed", target=".", method="_on_start_pressed"),
                    ],
                ),
                Button(
                    "ExitButton",
                    text="Exit",
                    position=Vec2(330, 320),
                    size=Vec2(140, 44),
                    signals=[
                        signal("pressed", target=".", method="_on_exit_pressed"),
                    ],
                ),
            ],
        ),
    )
)

game.add_scene(
    Scene(
        path="res://scenes/pong.tscn",
        root=Node2D(
            "Main",
            script=PONG_SCRIPT,
            children=[
                ColorRect(
                    "Background",
                    position=Vec2(0, 0),
                    size=Vec2(800, 600),
                    color=Color(0.03, 0.04, 0.05),
                ),
                ColorRect(
                    "LeftPaddle",
                    position=Vec2(32, 252),
                    size=Vec2(18, 96),
                    color=Color(0.9, 0.95, 1.0),
                ),
                ColorRect(
                    "RightPaddle",
                    position=Vec2(750, 252),
                    size=Vec2(18, 96),
                    color=Color(1.0, 0.86, 0.45),
                ),
                ColorRect(
                    "Ball",
                    position=Vec2(392, 292),
                    size=Vec2(16, 16),
                    color=Color(1.0, 1.0, 1.0),
                ),
                Label(
                    "LeftScore",
                    text="0",
                    position=Vec2(330, 28),
                ),
                Label(
                    "RightScore",
                    text="0",
                    position=Vec2(455, 28),
                ),
                Label(
                    "HelpText",
                    text="W/S and Up/Down move paddles. Space restarts.",
                    position=Vec2(215, 560),
                ),
            ],
        ),
    )
)

if __name__ == "__main__":
    game.run()
