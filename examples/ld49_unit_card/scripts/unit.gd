@onready var sprite := $AnimatedUnit
@onready var spawn_audio := $SpawnAudio
@onready var death_audio := $DeathAudio

func _ready() -> void:
    sprite.play("idle")

func play_spawn() -> void:
    spawn_audio.play()

func play_death() -> void:
    sprite.play("death")
    death_audio.play()

func _on_unit_input_event(_viewport, event: InputEvent, _shape_idx: int) -> void:
    if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
        play_death()
