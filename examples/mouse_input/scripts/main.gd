var clicks := 0

func _ready() -> void:
    _update_counter()

func _process(_delta: float) -> void:
    if Input.is_action_just_pressed("place_marker"):
        clicks += 1
        $Marker.position = get_viewport().get_mouse_position()
        _update_counter()

func _update_counter() -> void:
    $Counter.text = "clicks: %s" % clicks
