const SPEED := 520.0

var hit := false

func _physics_process(delta: float) -> void:
    if hit:
        return
    $Probe.position.x += SPEED * delta

func _on_probe_area_entered(area: Area2D) -> void:
    if area.name != "Goal":
        return
    hit = true
    print("pygodot_physics_area_entered")
    $Status.text = "area_entered: Probe hit Goal"
    $Probe/ProbeVisual.color = Color(0.45, 1.0, 0.58)
