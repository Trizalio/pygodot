const GRAVITY := 1450.0
const FLAP_VELOCITY := -430.0
const PIPE_SPEED := 190.0
const PIPE_RESET_X := 660.0
const PIPE_OFFSCREEN_X := -80.0
const PIPE_GAP := 180.0
const PIPE_HEIGHT := 480.0
const BIRD_START := Vector2(140, 310)

var bird_velocity := 0.0
var running := true
var score := 0
var pipe_a_scored := false
var pipe_b_scored := false
var pulse := 0

func _ready() -> void:
    reset_game()

func _physics_process(delta: float) -> void:
    if Input.is_action_just_pressed("restart"):
        reset_game()

    if not running:
        return

    if Input.is_action_just_pressed("flap"):
        bird_velocity = FLAP_VELOCITY

    bird_velocity += GRAVITY * delta
    $Bird.position.y += bird_velocity * delta

    move_pipe_pair("A", delta)
    move_pipe_pair("B", delta)
    update_score()

    if $Bird.position.y < 20:
        $Bird.position.y = 20
        bird_velocity = 0

func move_pipe_pair(pair: String, delta: float) -> void:
    var top := get_node("PipeTop%s" % pair)
    var bottom := get_node("PipeBottom%s" % pair)
    top.position.x -= PIPE_SPEED * delta
    bottom.position.x = top.position.x
    if top.position.x < PIPE_OFFSCREEN_X:
        reset_pipe_pair(pair, PIPE_RESET_X)

func reset_pipe_pair(pair: String, x: float) -> void:
    var gap_y := 250.0 + float((score + pulse + pair.unicode_at(0)) % 4) * 55.0
    var top := get_node("PipeTop%s" % pair)
    var bottom := get_node("PipeBottom%s" % pair)
    top.position = Vector2(x, gap_y - PIPE_GAP / 2.0 - PIPE_HEIGHT / 2.0)
    bottom.position = Vector2(x, gap_y + PIPE_GAP / 2.0 + PIPE_HEIGHT / 2.0)
    if pair == "A":
        pipe_a_scored = false
    else:
        pipe_b_scored = false

func update_score() -> void:
    if not pipe_a_scored and $PipeTopA.position.x < $Bird.position.x:
        pipe_a_scored = true
        add_score()
    if not pipe_b_scored and $PipeTopB.position.x < $Bird.position.x:
        pipe_b_scored = true
        add_score()

func add_score() -> void:
    score += 1
    $ScoreLabel.text = "Score: %s" % score

func game_over() -> void:
    if not running:
        return
    running = false
    $StateLabel.visible = true
    $StateLabel.text = "Game over - press R"
    $Bird/BirdVisual.color = Color(1.0, 0.34, 0.28)
    print("pygodot_flappy_game_over")

func reset_game() -> void:
    running = true
    score = 0
    bird_velocity = 0
    pipe_a_scored = false
    pipe_b_scored = false
    $Bird.position = BIRD_START
    $Bird/BirdVisual.color = Color(1.0, 0.82, 0.24)
    $ScoreLabel.text = "Score: 0"
    $StateLabel.visible = true
    $StateLabel.text = "Space/Up to flap"
    reset_pipe_pair("A", 560)
    reset_pipe_pair("B", 850)

func _on_bird_area_entered(area: Area2D) -> void:
    if area.name == "Ground" or area.name.begins_with("Pipe"):
        game_over()

func _on_spawn_timer_timeout() -> void:
    pulse += 1
    if running:
        $StateLabel.visible = pulse % 2 == 0
