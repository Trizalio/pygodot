extends Node

var rng := RandomNumberGenerator.new()
var last_seed := 0

func set_seed(seed: int) -> void:
    last_seed = seed
    rng.seed = seed

func roll(max_exclusive: int) -> int:
    if max_exclusive <= 0:
        return 0
    return rng.randi_range(0, max_exclusive - 1)

func choose(items: Array) -> Variant:
    if items.is_empty():
        return null
    return items[roll(items.size())]

func chance(percent: float) -> bool:
    return rng.randf() * 100.0 < percent
